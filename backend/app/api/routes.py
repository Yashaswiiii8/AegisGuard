from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db, verify_database_connection
from app.schemas.payment import (
    CustomerCreate,
    CustomerDeviceCreate,
    CustomerDeviceRead,
    CustomerRead,
    DeviceCreate,
    DeviceRead,
    MerchantCreate,
    MerchantRead,
    NetworkIdentityCreate,
    NetworkIdentityRead,
    TransactionCreate,
    TransactionRead,
)
from app.schemas.risk import RiskRuleCreate, RiskRuleRead, RiskSignalCreate, RiskSignalRead, RuleEvaluationRead
from app.services.payment_service import PaymentService
from app.services.risk_rules import RiskRuleService
from app.services.risk_signals import RiskSignalService
from app.services.rule_evaluation import RuleEvaluationService

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/health/db")
def database_health() -> dict[str, str]:
    try:
        verify_database_connection()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed",
        ) from exc
    return {"status": "ok", "database": "connected"}


@router.post("/customers", response_model=CustomerRead, status_code=status.HTTP_201_CREATED)
def create_customer(payload: CustomerCreate, db: Session = Depends(get_db)) -> CustomerRead:
    customer = PaymentService.create_customer(db, status=payload.status)
    return CustomerRead.model_validate(customer)


@router.post("/merchants", response_model=MerchantRead, status_code=status.HTTP_201_CREATED)
def create_merchant(payload: MerchantCreate, db: Session = Depends(get_db)) -> MerchantRead:
    merchant = PaymentService.create_merchant(db, status=payload.status)
    return MerchantRead.model_validate(merchant)


@router.post("/devices", response_model=DeviceRead, status_code=status.HTTP_201_CREATED)
def create_device(payload: DeviceCreate, db: Session = Depends(get_db)) -> DeviceRead:
    device = PaymentService.create_device(db, fingerprint=payload.fingerprint, device_type=payload.device_type)
    return DeviceRead.model_validate(device)


@router.post(
    "/network-identities",
    response_model=NetworkIdentityRead,
    status_code=status.HTTP_201_CREATED,
)
def create_network_identity(
    payload: NetworkIdentityCreate,
    db: Session = Depends(get_db),
) -> NetworkIdentityRead:
    network_identity = PaymentService.create_network_identity(
        db,
        identity_value=payload.identity_value,
        identity_type=payload.identity_type,
        country_code=payload.country_code,
    )
    return NetworkIdentityRead.model_validate(network_identity)


@router.post(
    "/customer-devices",
    response_model=CustomerDeviceRead,
    status_code=status.HTTP_201_CREATED,
)
def create_customer_device(
    payload: CustomerDeviceCreate,
    db: Session = Depends(get_db),
) -> CustomerDeviceRead:
    customer_device = PaymentService.create_customer_device(
        db,
        customer_id=payload.customer_id,
        device_id=payload.device_id,
        first_seen_at=payload.first_seen_at,
        last_seen_at=payload.last_seen_at,
    )
    return CustomerDeviceRead.model_validate(customer_device)


@router.post(
    "/transactions",
    response_model=TransactionRead,
    status_code=status.HTTP_201_CREATED,
)
def create_transaction(
    payload: TransactionCreate,
    db: Session = Depends(get_db),
) -> TransactionRead:
    transaction = PaymentService.create_transaction(
        db,
        customer_id=payload.customer_id,
        merchant_id=payload.merchant_id,
        amount_minor=payload.amount_minor,
        currency=payload.currency,
        payment_method=payload.payment_method,
        device_id=payload.device_id,
        network_identity_id=payload.network_identity_id,
        country_code=payload.country_code,
        status=payload.status,
        occurred_at=payload.occurred_at,
        available_at=payload.available_at,
    )
    return TransactionRead.model_validate(transaction)


@router.get("/transactions/{transaction_id}", response_model=TransactionRead)
def get_transaction(transaction_id: UUID, db: Session = Depends(get_db)) -> TransactionRead:
    transaction = PaymentService.get_transaction(db, transaction_id)
    return TransactionRead.model_validate(transaction)


@router.post("/risk-signals", response_model=RiskSignalRead, status_code=status.HTTP_201_CREATED)
def create_risk_signal(
    payload: RiskSignalCreate, db: Session = Depends(get_db)
) -> RiskSignalRead:
    signal = RiskSignalService.create(db, **payload.model_dump())
    return RiskSignalRead.model_validate(signal)


@router.get("/risk-signals/{signal_id}", response_model=RiskSignalRead)
def get_risk_signal(signal_id: UUID, db: Session = Depends(get_db)) -> RiskSignalRead:
    return RiskSignalRead.model_validate(RiskSignalService.get(db, signal_id))


@router.post("/risk-rules", response_model=RiskRuleRead, status_code=status.HTTP_201_CREATED)
def create_risk_rule(payload: RiskRuleCreate, db: Session = Depends(get_db)) -> RiskRuleRead:
    rule = RiskRuleService.create(db, **payload.model_dump())
    return RiskRuleRead.model_validate(rule)


@router.get("/risk-rules/{rule_id}", response_model=RiskRuleRead)
def get_risk_rule(rule_id: UUID, db: Session = Depends(get_db)) -> RiskRuleRead:
    return RiskRuleRead.model_validate(RiskRuleService.get(db, rule_id))


@router.post(
    "/risk-rules/{rule_id}/evaluate/{transaction_id}",
    response_model=RuleEvaluationRead,
    status_code=status.HTTP_201_CREATED,
)
def evaluate_risk_rule(
    rule_id: UUID, transaction_id: UUID, db: Session = Depends(get_db)
) -> RuleEvaluationRead:
    evaluation = RuleEvaluationService.evaluate(db, rule_id, transaction_id)
    return RuleEvaluationRead.model_validate(evaluation)


@router.get("/rule-evaluations/{evaluation_id}", response_model=RuleEvaluationRead)
def get_rule_evaluation(
    evaluation_id: UUID, db: Session = Depends(get_db)
) -> RuleEvaluationRead:
    return RuleEvaluationRead.model_validate(RuleEvaluationService.get(db, evaluation_id))
