from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.payment import RiskRule, RuleEvaluation, Transaction
from app.services.velocity import VelocityCalculator


class RuleEvaluationService:
    @staticmethod
    def evaluate(db: Session, rule_id: UUID, transaction_id: UUID) -> RuleEvaluation:
        rule = db.get(RiskRule, rule_id)
        if rule is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RiskRule not found")
        if not rule.enabled:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="RiskRule is disabled")
        transaction = db.get(Transaction, transaction_id)
        if transaction is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
        if rule.rule_type != "CUSTOMER_TRANSACTION_VELOCITY":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported rule type")
        window_seconds = int(rule.configuration["window_seconds"])
        threshold = int(rule.configuration["threshold"])
        observation = VelocityCalculator.calculate(
            db,
            customer_id=transaction.customer_id,
            occurred_at=transaction.occurred_at,
            available_at=transaction.available_at,
            window_seconds=window_seconds,
        )
        evaluation = RuleEvaluation(
            rule_id=rule.id,
            transaction_id=transaction.id,
            rule_version=rule.version,
            triggered=observation.transaction_count > threshold,
            configuration_snapshot=dict(rule.configuration),
            details={
                "transaction_count": observation.transaction_count,
                "window_seconds": observation.window_seconds,
                "threshold": threshold,
            },
        )
        db.add(evaluation)
        db.commit()
        db.refresh(evaluation)
        return evaluation

    @staticmethod
    def get(db: Session, evaluation_id: UUID) -> RuleEvaluation:
        evaluation = db.get(RuleEvaluation, evaluation_id)
        if evaluation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="RuleEvaluation not found",
            )
        return evaluation
