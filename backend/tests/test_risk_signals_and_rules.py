from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.db.session import SessionLocal
from app.main import app
from app.models.payment import RiskRule, RuleEvaluation, Transaction
from app.services.risk_signals import RiskSignalService
from app.services.velocity import VelocityCalculator, VelocityObservation

client = TestClient(app)


def create_payment_entities() -> tuple[str, str, str, str]:
    customer = client.post("/customers", json={}).json()
    merchant = client.post("/merchants", json={}).json()
    device = client.post(
        "/devices",
        json={"fingerprint": str(uuid4()), "device_type": "mobile"},
    ).json()
    network = client.post(
        "/network-identities",
        json={
            "identity_value": f"198.51.100.{uuid4().int % 200 + 1}",
            "identity_type": "ip_address",
            "country_code": "US",
        },
    ).json()
    return customer["id"], merchant["id"], device["id"], network["id"]


def create_transaction(
    customer_id: str,
    merchant_id: str,
    device_id: str,
    network_id: str,
    occurred_at: datetime,
    available_at: datetime | None = None,
) -> dict:
    if available_at is None:
        available_at = occurred_at
    response = client.post(
        "/transactions",
        json={
            "customer_id": customer_id,
            "merchant_id": merchant_id,
            "amount_minor": 100,
            "currency": "USD",
            "payment_method": "card",
            "device_id": device_id,
            "network_identity_id": network_id,
            "country_code": "US",
            "status": "authorized",
            "occurred_at": occurred_at.isoformat(),
            "available_at": available_at.isoformat(),
        },
    )
    assert response.status_code == 201, response.text
    return response.json()


def create_velocity_rule(
    threshold: int = 5,
    window_seconds: int = 600,
    enabled: bool = True,
) -> dict:
    response = client.post(
        "/risk-rules",
        json={
            "name": "CUSTOMER_TRANSACTION_VELOCITY",
            "description": "Customer transaction velocity",
            "rule_type": "CUSTOMER_TRANSACTION_VELOCITY",
            "version": 1,
            "configuration": {
                "threshold": threshold,
                "window_seconds": window_seconds,
            },
            "enabled": enabled,
        },
    )
    assert response.status_code == 201, response.text
    return response.json()


def test_risk_signal_create_retrieve_and_payload() -> None:
    customer_id, merchant_id, device_id, network_id = create_payment_entities()
    transaction = create_transaction(
        customer_id,
        merchant_id,
        device_id,
        network_id,
        datetime(2024, 1, 1, 10, 0, tzinfo=timezone.utc),
    )
    occurred_at = datetime(2024, 1, 1, 10, 0, tzinfo=timezone(timedelta(hours=5, minutes=30)))
    available_at = datetime(2024, 1, 1, 10, 5, tzinfo=timezone(timedelta(hours=5, minutes=30)))
    response = client.post(
        "/risk-signals",
        json={
            "transaction_id": transaction["id"],
            "signal_type": "HIGH_VELOCITY",
            "source": "RULE_ENGINE",
            "value": {"transaction_count": 8, "window_seconds": 600, "threshold": 5},
            "occurred_at": occurred_at.isoformat(),
            "available_at": available_at.isoformat(),
        },
    )
    assert response.status_code == 201, response.text
    signal = response.json()
    assert signal["value"]["transaction_count"] == 8
    assert datetime.fromisoformat(signal["occurred_at"].replace("Z", "+00:00")).utcoffset() == timedelta(0)
    assert datetime.fromisoformat(signal["available_at"].replace("Z", "+00:00")).utcoffset() == timedelta(0)
    retrieved = client.get(f"/risk-signals/{signal['id']}")
    assert retrieved.status_code == 200
    assert retrieved.json()["value"]["threshold"] == 5


def test_risk_signal_rejects_invalid_transaction_and_naive_timestamp() -> None:
    response = client.post(
        "/risk-signals",
        json={
            "transaction_id": str(uuid4()),
            "signal_type": "HIGH_VELOCITY",
            "source": "RULE_ENGINE",
            "value": {"transaction_count": 8},
            "occurred_at": "2024-01-01T10:00:00",
            "available_at": "2024-01-01T10:05:00Z",
        },
    )
    assert response.status_code == 422
    assert "Timestamp must include a timezone offset" in response.text

    customer_id, merchant_id, device_id, network_id = create_payment_entities()
    transaction = create_transaction(
        customer_id,
        merchant_id,
        device_id,
        network_id,
        datetime(2024, 1, 1, 10, 0, tzinfo=timezone.utc),
    )
    response = client.post(
        "/risk-signals",
        json={
            "transaction_id": transaction["id"],
            "signal_type": "HIGH_VELOCITY",
            "source": "RULE_ENGINE",
            "value": {"transaction_count": 8},
            "occurred_at": "2024-01-01T10:00:00Z",
            "available_at": "2024-01-01T10:05:00Z",
        },
    )
    assert response.status_code == 201

    response = client.post(
        "/risk-signals",
        json={
            "transaction_id": str(uuid4()),
            "signal_type": "HIGH_VELOCITY",
            "source": "RULE_ENGINE",
            "value": {"transaction_count": 8},
            "occurred_at": "2024-01-01T10:00:00Z",
            "available_at": "2024-01-01T10:05:00Z",
        },
    )
    assert response.status_code == 404


@pytest.mark.parametrize("transaction_count, expected_signal", [(5, False), (6, True)])
def test_customer_velocity_signal_threshold(
    transaction_count: int, expected_signal: bool
) -> None:
    customer_id, merchant_id, device_id, network_id = create_payment_entities()
    start = datetime(2024, 1, 1, 10, 0, tzinfo=timezone.utc)
    transactions = [
        create_transaction(
            customer_id,
            merchant_id,
            device_id,
            network_id,
            start + timedelta(seconds=index * 60),
        )
        for index in range(transaction_count)
    ]
    with SessionLocal() as db:
        transaction = db.get(Transaction, UUID(transactions[-1]["id"]))
        assert transaction is not None
        signal = RiskSignalService.generate_high_velocity(
            db, transaction, window_seconds=600, threshold=5
        )
        assert (signal is not None) is expected_signal
        if signal is not None:
            assert signal.value == {
                "transaction_count": 6,
                "window_seconds": 600,
                "threshold": 5,
            }


def test_velocity_excludes_future_transactions() -> None:
    customer_id, merchant_id, device_id, network_id = create_payment_entities()
    start = datetime(2024, 1, 1, 10, 0, tzinfo=timezone.utc)
    first_five = [
        create_transaction(
            customer_id, merchant_id, device_id, network_id, start + timedelta(minutes=index)
        )
        for index in range(5)
    ]
    future = create_transaction(
        customer_id, merchant_id, device_id, network_id, start + timedelta(minutes=6)
    )
    with SessionLocal() as db:
        transaction = db.get(Transaction, UUID(first_five[-1]["id"]))
        assert transaction is not None
        signal = RiskSignalService.generate_high_velocity(
            db, transaction, window_seconds=600, threshold=5
        )
        assert signal is None
        assert future["id"] != first_five[-1]["id"]


def test_velocity_calculator_excludes_unavailable_transactions() -> None:
    customer_id, merchant_id, device_id, network_id = create_payment_entities()
    start = datetime(2024, 1, 1, 10, 0, tzinfo=timezone.utc)
    target = create_transaction(
        customer_id, merchant_id, device_id, network_id, start + timedelta(minutes=5)
    )
    create_transaction(
        customer_id,
        merchant_id,
        device_id,
        network_id,
        start + timedelta(minutes=4),
        available_at=start + timedelta(minutes=6),
    )
    with SessionLocal() as db:
        observation = VelocityCalculator.calculate(
            db,
            customer_id=UUID(customer_id),
            occurred_at=start + timedelta(minutes=5),
            available_at=start + timedelta(minutes=5),
            window_seconds=600,
        )
        assert observation == VelocityObservation(transaction_count=1, window_seconds=600)
        assert target["customer_id"] == customer_id


def test_signal_generator_uses_shared_velocity_calculator() -> None:
    customer_id, merchant_id, device_id, network_id = create_payment_entities()
    transaction = create_transaction(
        customer_id, merchant_id, device_id, network_id, datetime.now(timezone.utc)
    )
    with SessionLocal() as db, patch(
        "app.services.risk_signals.VelocityCalculator.calculate",
        return_value=VelocityObservation(transaction_count=6, window_seconds=600),
    ) as calculate:
        persisted_transaction = db.get(Transaction, UUID(transaction["id"]))
        assert persisted_transaction is not None
        signal = RiskSignalService.generate_high_velocity(
            db, persisted_transaction, window_seconds=600, threshold=5
        )
        assert signal is not None
        calculate.assert_called_once()
        assert signal.value["transaction_count"] == 6


def test_rule_evaluator_uses_shared_velocity_calculator() -> None:
    customer_id, merchant_id, device_id, network_id = create_payment_entities()
    transaction = create_transaction(
        customer_id, merchant_id, device_id, network_id, datetime.now(timezone.utc)
    )
    rule = create_velocity_rule()
    with patch(
        "app.services.rule_evaluation.VelocityCalculator.calculate",
        return_value=VelocityObservation(transaction_count=6, window_seconds=600),
    ) as calculate:
        response = client.post(f"/risk-rules/{rule['id']}/evaluate/{transaction['id']}")
        assert response.status_code == 201, response.text
        calculate.assert_called_once()
        assert response.json()["triggered"] is True


def test_signal_generation_and_rule_evaluation_remain_separate() -> None:
    customer_id, merchant_id, device_id, network_id = create_payment_entities()
    transaction = create_transaction(
        customer_id, merchant_id, device_id, network_id, datetime.now(timezone.utc)
    )
    rule = create_velocity_rule()
    with SessionLocal() as db, patch(
        "app.services.risk_signals.VelocityCalculator.calculate",
        return_value=VelocityObservation(transaction_count=6, window_seconds=600),
    ):
        persisted_transaction = db.get(Transaction, UUID(transaction["id"]))
        assert persisted_transaction is not None
        signal = RiskSignalService.generate_high_velocity(
            db, persisted_transaction, window_seconds=600, threshold=5
        )
        assert signal is not None
        assert db.query(RuleEvaluation).count() == 0
    response = client.post(f"/risk-rules/{rule['id']}/evaluate/{transaction['id']}")
    assert response.status_code == 201
    with SessionLocal() as db:
        assert db.query(RuleEvaluation).count() == 1


def test_risk_rule_create_retrieve_and_configuration() -> None:
    rule = create_velocity_rule()
    assert rule["configuration"] == {"threshold": 5, "window_seconds": 600}
    retrieved = client.get(f"/risk-rules/{rule['id']}")
    assert retrieved.status_code == 200
    assert retrieved.json()["version"] == 1


def test_disabled_rule_cannot_be_evaluated() -> None:
    customer_id, merchant_id, device_id, network_id = create_payment_entities()
    transaction = create_transaction(
        customer_id, merchant_id, device_id, network_id, datetime.now(timezone.utc)
    )
    rule = create_velocity_rule(enabled=False)
    response = client.post(f"/risk-rules/{rule['id']}/evaluate/{transaction['id']}")
    assert response.status_code == 409


def test_rule_evaluation_persists_result_and_configuration_snapshot() -> None:
    customer_id, merchant_id, device_id, network_id = create_payment_entities()
    start = datetime(2024, 1, 1, 10, 0, tzinfo=timezone.utc)
    transactions = [
        create_transaction(
            customer_id, merchant_id, device_id, network_id, start + timedelta(minutes=index)
        )
        for index in range(6)
    ]
    rule = create_velocity_rule()
    response = client.post(f"/risk-rules/{rule['id']}/evaluate/{transactions[-1]['id']}")
    assert response.status_code == 201, response.text
    evaluation = response.json()
    assert evaluation["triggered"] is True
    assert evaluation["rule_version"] == 1
    assert evaluation["configuration_snapshot"] == {
        "threshold": 5,
        "window_seconds": 600,
    }
    assert evaluation["details"]["transaction_count"] == 6
    retrieved = client.get(f"/rule-evaluations/{evaluation['id']}")
    assert retrieved.status_code == 200

    with SessionLocal() as db:
        persisted_rule = db.get(RiskRule, UUID(rule["id"]))
        persisted_evaluation = db.get(RuleEvaluation, UUID(evaluation["id"]))
        assert persisted_rule is not None
        assert persisted_evaluation is not None
        persisted_rule.configuration = {"threshold": 10, "window_seconds": 1200}
        persisted_rule.version = 2
        db.commit()
        db.refresh(persisted_evaluation)
        assert persisted_evaluation.rule_version == 1
        assert persisted_evaluation.configuration_snapshot == {
            "threshold": 5,
            "window_seconds": 600,
        }
