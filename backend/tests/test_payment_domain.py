from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.db.session import SessionLocal
from app.main import app
from app.models.payment import Customer, CustomerDevice, Device, Merchant, NetworkIdentity, Transaction

client = TestClient(app)


@pytest.fixture
def payment_client() -> TestClient:
    return client


def _create_customer(status: str = "active") -> dict:
    response = client.post("/customers", json={"status": status})
    assert response.status_code == 201, response.text
    return response.json()


def _create_merchant(status: str = "active") -> dict:
    response = client.post("/merchants", json={"status": status})
    assert response.status_code == 201, response.text
    return response.json()


def _create_device(fingerprint: str, device_type: str = "mobile") -> dict:
    response = client.post("/devices", json={"fingerprint": fingerprint, "device_type": device_type})
    assert response.status_code == 201, response.text
    return response.json()


def _create_network_identity(identity_value: str, identity_type: str = "ip_address", country_code: str = "US") -> dict:
    response = client.post(
        "/network-identities",
        json={
            "identity_value": identity_value,
            "identity_type": identity_type,
            "country_code": country_code,
        },
    )
    assert response.status_code == 201, response.text
    return response.json()


def _create_customer_device(customer_id: str, device_id: str) -> dict:
    first_seen_at = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
    last_seen_at = datetime(2024, 1, 1, 12, 15, tzinfo=timezone.utc)
    response = client.post(
        "/customer-devices",
        json={
            "customer_id": customer_id,
            "device_id": device_id,
            "first_seen_at": first_seen_at.isoformat(),
            "last_seen_at": last_seen_at.isoformat(),
        },
    )
    assert response.status_code == 201, response.text
    return response.json()


def _create_transaction_payload(
    customer_id: str,
    merchant_id: str,
    device_id: str,
    network_identity_id: str,
    *,
    amount_minor: int = 125075,
    currency: str = "INR",
    occurred_at: datetime | None = None,
    created_at: datetime | None = None,
    available_at: datetime | None = None,
    status: str = "authorized",
    payment_method: str = "card",
    country_code: str = "IN",
) -> dict:
    now = datetime.now(timezone.utc)
    if occurred_at is None:
        occurred_at = now - timedelta(minutes=5)
    if created_at is None:
        created_at = now
    if available_at is None:
        available_at = now + timedelta(minutes=1)

    return {
        "customer_id": customer_id,
        "merchant_id": merchant_id,
        "amount_minor": amount_minor,
        "currency": currency,
        "payment_method": payment_method,
        "device_id": device_id,
        "network_identity_id": network_identity_id,
        "country_code": country_code,
        "status": status,
        "occurred_at": occurred_at.isoformat(),
        "created_at": created_at.isoformat(),
        "available_at": available_at.isoformat(),
    }


def test_customer_creation_and_availability(payment_client: TestClient) -> None:
    payload = _create_customer()
    assert payload["status"] == "active"
    with SessionLocal() as db:
        customer = db.get(Customer, UUID(payload["id"]))
        assert customer is not None
        assert customer.status == "active"


def test_merchant_creation_and_availability(payment_client: TestClient) -> None:
    payload = _create_merchant()
    assert payload["status"] == "active"
    with SessionLocal() as db:
        merchant = db.get(Merchant, UUID(payload["id"]))
        assert merchant is not None
        assert merchant.status == "active"


def test_device_creation_and_availability(payment_client: TestClient) -> None:
    payload = _create_device("device-001", "mobile")
    assert payload["fingerprint"] == "device-001"
    with SessionLocal() as db:
        device = db.query(Device).filter_by(fingerprint="device-001").one()
        assert device.device_type == "mobile"


def test_network_identity_creation_and_availability(payment_client: TestClient) -> None:
    payload = _create_network_identity("203.0.113.9", "ip_address", "US")
    assert payload["identity_value"] == "203.0.113.9"
    with SessionLocal() as db:
        identity = db.query(NetworkIdentity).filter_by(identity_value="203.0.113.9").one()
        assert identity.country_code == "US"


def test_customer_device_relationship(payment_client: TestClient) -> None:
    customer = _create_customer()
    device = _create_device("device-002")
    payload = _create_customer_device(customer["id"], device["id"])
    assert payload["customer_id"] == customer["id"]
    assert payload["device_id"] == device["id"]
    with SessionLocal() as db:
        link = db.get(CustomerDevice, (UUID(customer["id"]), UUID(device["id"])))
        assert link is not None
        assert link.customer_id == UUID(customer["id"])
        assert link.device_id == UUID(device["id"])


def test_successful_transaction_creation(payment_client: TestClient) -> None:
    customer = _create_customer()
    merchant = _create_merchant()
    device = _create_device("device-003")
    network_identity = _create_network_identity("198.51.100.11", "ip_address", "US")
    payload = _create_transaction_payload(
        customer["id"], merchant["id"], device["id"], network_identity["id"], amount_minor=125075
    )
    response = client.post("/transactions", json=payload)
    assert response.status_code == 201, response.text
    body = response.json()
    assert body["customer_id"] == customer["id"]
    assert body["merchant_id"] == merchant["id"]
    assert body["device_id"] == device["id"]
    assert body["network_identity_id"] == network_identity["id"]
    assert body["amount_minor"] == 125075
    assert body["currency"] == "INR"


def test_transaction_retrieval(payment_client: TestClient) -> None:
    customer = _create_customer()
    merchant = _create_merchant()
    device = _create_device("device-004")
    network_identity = _create_network_identity("198.51.100.12", "ip_address", "US")
    payload = _create_transaction_payload(
        customer["id"], merchant["id"], device["id"], network_identity["id"], amount_minor=99
    )
    created = client.post("/transactions", json=payload)
    transaction_id = created.json()["id"]
    response = client.get(f"/transactions/{transaction_id}")
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["id"] == transaction_id
    assert body["amount_minor"] == 99
    assert body["currency"] == "INR"


def test_rejects_missing_referenced_entity(payment_client: TestClient) -> None:
    customer = _create_customer()
    merchant = _create_merchant()
    device = _create_device("device-005")
    network_identity = _create_network_identity("198.51.100.13", "ip_address", "US")
    payload = _create_transaction_payload(
        customer["id"], merchant["id"], str(uuid4()), network_identity["id"]
    )
    response = client.post("/transactions", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Device not found"


def test_transaction_uses_amount_minor_and_currency(payment_client: TestClient) -> None:
    customer = _create_customer()
    merchant = _create_merchant()
    device = _create_device("device-006")
    network_identity = _create_network_identity("198.51.100.14", "ip_address", "US")
    payload = _create_transaction_payload(
        customer["id"], merchant["id"], device["id"], network_identity["id"], amount_minor=2500, currency="usd"
    )
    response = client.post("/transactions", json=payload)
    assert response.status_code == 201, response.text
    body = response.json()
    assert isinstance(body["amount_minor"], int)
    assert body["amount_minor"] == 2500
    assert body["currency"] == "USD"


def test_transaction_preserves_occurred_created_and_available_times(payment_client: TestClient) -> None:
    customer = _create_customer()
    merchant = _create_merchant()
    device = _create_device("device-007")
    network_identity = _create_network_identity("198.51.100.15", "ip_address", "US")
    occurred_at = datetime(2024, 7, 15, 8, 30, tzinfo=timezone.utc)
    created_at = datetime(2024, 7, 15, 8, 31, tzinfo=timezone.utc)
    available_at = datetime(2024, 7, 15, 8, 45, tzinfo=timezone.utc)
    payload = _create_transaction_payload(
        customer["id"], merchant["id"], device["id"], network_identity["id"], occurred_at=occurred_at, created_at=created_at, available_at=available_at
    )
    response = client.post("/transactions", json=payload)
    assert response.status_code == 201, response.text
    body = response.json()
    assert datetime.fromisoformat(body["occurred_at"]).astimezone(timezone.utc) == occurred_at
    assert datetime.fromisoformat(body["created_at"]).astimezone(timezone.utc) == created_at
    assert datetime.fromisoformat(body["available_at"]).astimezone(timezone.utc) == available_at


def test_transaction_table_has_expected_columns() -> None:
    with SessionLocal() as db:
        result = db.execute(
            text(
                "SELECT column_name FROM information_schema.columns WHERE table_name = 'transactions' ORDER BY ordinal_position"
            )
        )
        columns = {row[0] for row in result}
        assert {"id", "customer_id", "merchant_id", "amount_minor", "currency", "payment_method", "device_id", "network_identity_id", "country_code", "status", "occurred_at", "created_at", "available_at"}.issubset(columns)
