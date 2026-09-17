from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.payment import Transaction


@dataclass(frozen=True)
class VelocityObservation:
    transaction_count: int
    window_seconds: int


class VelocityCalculator:
    @staticmethod
    def calculate(
        db: Session,
        *,
        customer_id: UUID,
        occurred_at: datetime,
        available_at: datetime,
        window_seconds: int,
    ) -> VelocityObservation:
        window_start = occurred_at - timedelta(seconds=window_seconds)
        transaction_count = db.scalar(
            select(func.count(Transaction.id)).where(
                Transaction.customer_id == customer_id,
                Transaction.occurred_at >= window_start,
                Transaction.occurred_at <= occurred_at,
                Transaction.available_at <= available_at,
            )
        )
        return VelocityObservation(
            transaction_count=int(transaction_count or 0),
            window_seconds=window_seconds,
        )
