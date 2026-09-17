from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CustomerBase(BaseModel):
    status: str = "active"


class CustomerCreate(CustomerBase):
    pass


class CustomerRead(CustomerBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime


class MerchantBase(BaseModel):
    status: str = "active"


class MerchantCreate(MerchantBase):
    pass


class MerchantRead(MerchantBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime


class DeviceBase(BaseModel):
    fingerprint: str
    device_type: str


class DeviceCreate(DeviceBase):
    pass


class DeviceRead(DeviceBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime


class NetworkIdentityBase(BaseModel):
    identity_value: str
    identity_type: str
    country_code: str = Field(..., min_length=2, max_length=2)


class NetworkIdentityCreate(NetworkIdentityBase):
    pass


class NetworkIdentityRead(NetworkIdentityBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime

    @field_validator("country_code")
    @classmethod
    def validate_country_code(cls, value: str) -> str:
        return value.upper()


class CustomerDeviceBase(BaseModel):
    customer_id: UUID
    device_id: UUID
    first_seen_at: datetime
    last_seen_at: datetime


class CustomerDeviceCreate(CustomerDeviceBase):
    pass


class CustomerDeviceRead(CustomerDeviceBase):
    model_config = ConfigDict(from_attributes=True)


class TransactionFields(BaseModel):
    customer_id: UUID
    merchant_id: UUID
    amount_minor: int = Field(..., ge=0)
    currency: str = Field(..., min_length=3, max_length=3)
    payment_method: str
    device_id: UUID
    network_identity_id: UUID
    country_code: str = Field(..., min_length=2, max_length=2)
    status: str
    occurred_at: datetime
    available_at: datetime

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, value: str) -> str:
        return value.upper()

    @field_validator("country_code")
    @classmethod
    def validate_country_code(cls, value: str) -> str:
        return value.upper()

    @field_validator("occurred_at", "available_at")
    @classmethod
    def normalize_timestamp_to_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("Timestamp must include a timezone offset")
        return value.astimezone(timezone.utc)


class TransactionCreate(TransactionFields):
    pass


class TransactionRead(TransactionFields):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
