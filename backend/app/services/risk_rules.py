from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.payment import RiskRule


class RiskRuleService:
    @staticmethod
    def create(db: Session, **fields: object) -> RiskRule:
        rule = RiskRule(**fields)
        db.add(rule)
        db.commit()
        db.refresh(rule)
        return rule

    @staticmethod
    def get(db: Session, rule_id: UUID) -> RiskRule:
        rule = db.get(RiskRule, rule_id)
        if rule is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RiskRule not found")
        return rule
