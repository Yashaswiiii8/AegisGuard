from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import BigInteger, CheckConstraint, DateTime, ForeignKey, Index, String, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    transactions: Mapped[list["Transaction"]] = relationship(back_populates="customer")
    devices: Mapped[list["Device"]] = relationship(
        secondary="customer_devices",
        back_populates="customers",
        overlaps="customer_devices,customer,device",
    )
    customer_devices: Mapped[list["CustomerDevice"]] = relationship(
        back_populates="customer",
        overlaps="devices,customers",
    )


class Merchant(Base):
    __tablename__ = "merchants"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    transactions: Mapped[list["Transaction"]] = relationship(back_populates="merchant")


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    fingerprint: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    device_type: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    transactions: Mapped[list["Transaction"]] = relationship(back_populates="device")
    customers: Mapped[list[Customer]] = relationship(
        secondary="customer_devices",
        back_populates="devices",
        overlaps="customer_devices,customer,device",
    )
    customer_devices: Mapped[list["CustomerDevice"]] = relationship(
        back_populates="device",
        overlaps="devices,customers",
    )


class NetworkIdentity(Base):
    __tablename__ = "network_identities"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    identity_value: Mapped[str] = mapped_column(String(255), nullable=False)
    identity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    country_code: Mapped[str] = mapped_column(String(2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    transactions: Mapped[list["Transaction"]] = relationship(back_populates="network_identity")

    __table_args__ = (
        CheckConstraint("char_length(country_code) = 2", name="ck_network_identities_country_code_length"),
        Index("ix_network_identities_type_value", "identity_type", "identity_value", unique=True),
    )


class CustomerDevice(Base):
    __tablename__ = "customer_devices"

    customer_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("customers.id"), primary_key=True
    )
    device_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("devices.id"), primary_key=True
    )
    first_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    customer: Mapped[Customer] = relationship(
        back_populates="customer_devices",
        overlaps="devices,customers",
    )
    device: Mapped[Device] = relationship(
        back_populates="customer_devices",
        overlaps="devices,customers",
    )

    __table_args__ = (
        CheckConstraint("first_seen_at <= last_seen_at", name="ck_customer_devices_seen_order"),
    )


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    customer_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("customers.id"), nullable=False, index=True
    )
    merchant_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("merchants.id"), nullable=False, index=True
    )
    device_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("devices.id"), nullable=False, index=True
    )
    network_identity_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("network_identities.id"), nullable=False, index=True
    )
    amount_minor: Mapped[int] = mapped_column(BigInteger, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    payment_method: Mapped[str] = mapped_column(String(50), nullable=False)
    country_code: Mapped[str] = mapped_column(String(2), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    available_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )

    customer: Mapped[Customer] = relationship(back_populates="transactions")
    merchant: Mapped[Merchant] = relationship(back_populates="transactions")
    device: Mapped[Device] = relationship(back_populates="transactions")
    network_identity: Mapped[NetworkIdentity] = relationship(back_populates="transactions")

    __table_args__ = (
        CheckConstraint("amount_minor >= 0", name="ck_transactions_amount_non_negative"),
        CheckConstraint("char_length(currency) = 3", name="ck_transactions_currency_length"),
        CheckConstraint("char_length(country_code) = 2", name="ck_transactions_country_code_length"),
        Index("ix_transactions_customer_occurred", "customer_id", "occurred_at"),
        Index("ix_transactions_merchant_occurred", "merchant_id", "occurred_at"),
        Index("ix_transactions_device_occurred", "device_id", "occurred_at"),
        Index("ix_transactions_available_at", "available_at"),
    )
