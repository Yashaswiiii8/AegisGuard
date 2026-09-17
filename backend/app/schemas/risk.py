from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


def normalize_timestamp(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("Timestamp must include a timezone offset")
    return value.astimezone(timezone.utc)


class RiskSignalCreate(BaseModel):
    transaction_id: UUID | None = None
    signal_type: str
    source: str
    value: dict
    occurred_at: datetime
    available_at: datetime

    _normalize_timestamps = field_validator("occurred_at", "available_at")(
        normalize_timestamp
    )


class RiskSignalRead(RiskSignalCreate):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime


class RiskRuleCreate(BaseModel):
    name: str
    description: str
    rule_type: str
    version: int = Field(default=1, ge=1)
    configuration: dict
    enabled: bool = True


class RiskRuleRead(RiskRuleCreate):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime


class RuleEvaluationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    rule_id: UUID
    transaction_id: UUID
    rule_version: int
    triggered: bool
    evaluated_at: datetime
    configuration_snapshot: dict
    details: dict
