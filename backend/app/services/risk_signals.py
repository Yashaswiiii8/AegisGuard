from __future__ import annotations

from datetime import datetime
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.payment import RiskSignal, Transaction
from app.services.velocity import VelocityCalculator


class RiskSignalService:
    @staticmethod
    def create(
        db: Session,
        *,
        transaction_id: UUID | None,
        signal_type: str,
        source: str,
        value: dict,
        occurred_at: datetime,
        available_at: datetime,
    ) -> RiskSignal:
        if transaction_id is not None and db.get(Transaction, transaction_id) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
        signal = RiskSignal(
            transaction_id=transaction_id,
            signal_type=signal_type,
            source=source,
            value=value,
            occurred_at=occurred_at,
            available_at=available_at,
        )
        db.add(signal)
        db.commit()
        db.refresh(signal)
        return signal

    @staticmethod
    def get(db: Session, signal_id: UUID) -> RiskSignal:
        signal = db.get(RiskSignal, signal_id)
        if signal is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RiskSignal not found")
        return signal

    @staticmethod
    def generate_high_velocity(
        db: Session,
        transaction: Transaction,
        *,
        window_seconds: int,
        threshold: int,
    ) -> RiskSignal | None:
        observation = VelocityCalculator.calculate(
            db,
            customer_id=transaction.customer_id,
            occurred_at=transaction.occurred_at,
            available_at=transaction.available_at,
            window_seconds=window_seconds,
        )
        if observation.transaction_count <= threshold:
            return None
        return RiskSignalService.create(
            db,
            transaction_id=transaction.id,
            signal_type="HIGH_VELOCITY",
            source="RULE_ENGINE",
            value={
                "transaction_count": observation.transaction_count,
                "window_seconds": observation.window_seconds,
                "threshold": threshold,
            },
            occurred_at=transaction.occurred_at,
            available_at=transaction.available_at,
        )
