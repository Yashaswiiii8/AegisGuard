from __future__ import annotations

from datetime import datetime
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.payment import (
    Customer,
    CustomerDevice,
    Device,
    Merchant,
    NetworkIdentity,
    Transaction,
)


class PaymentService:
    @staticmethod
    def create_customer(db: Session, status: str = "active") -> Customer:
        customer = Customer(status=status)
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer

    @staticmethod
    def get_customer(db: Session, customer_id: UUID) -> Customer:
        customer = db.get(Customer, customer_id)
        if customer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found",
            )
        return customer

    @staticmethod
    def create_merchant(db: Session, status: str = "active") -> Merchant:
        merchant = Merchant(status=status)
        db.add(merchant)
        db.commit()
        db.refresh(merchant)
        return merchant

    @staticmethod
    def get_merchant(db: Session, merchant_id: UUID) -> Merchant:
        merchant = db.get(Merchant, merchant_id)
        if merchant is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Merchant not found",
            )
        return merchant

    @staticmethod
    def create_device(db: Session, fingerprint: str, device_type: str) -> Device:
        device = Device(fingerprint=fingerprint, device_type=device_type)
        db.add(device)
        db.commit()
        db.refresh(device)
        return device

    @staticmethod
    def get_device(db: Session, device_id: UUID) -> Device:
        device = db.get(Device, device_id)
        if device is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found",
            )
        return device

    @staticmethod
    def create_network_identity(
        db: Session,
        identity_value: str,
        identity_type: str,
        country_code: str,
    ) -> NetworkIdentity:
        network_identity = NetworkIdentity(
            identity_value=identity_value,
            identity_type=identity_type,
            country_code=country_code.upper(),
        )
        db.add(network_identity)
        db.commit()
        db.refresh(network_identity)
        return network_identity

    @staticmethod
    def get_network_identity(db: Session, network_identity_id: UUID) -> NetworkIdentity:
        network_identity = db.get(NetworkIdentity, network_identity_id)
        if network_identity is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="NetworkIdentity not found",
            )
        return network_identity

    @staticmethod
    def create_customer_device(
        db: Session,
        customer_id: UUID,
        device_id: UUID,
        first_seen_at: datetime,
        last_seen_at: datetime,
    ) -> CustomerDevice:
        customer = PaymentService.get_customer(db, customer_id)
        device = PaymentService.get_device(db, device_id)
        customer_device = CustomerDevice(
            customer_id=customer.id,
            device_id=device.id,
            first_seen_at=first_seen_at,
            last_seen_at=last_seen_at,
        )
        db.add(customer_device)
        db.commit()
        db.refresh(customer_device)
        return customer_device

    @staticmethod
    def create_transaction(
        db: Session,
        *,
        customer_id: UUID,
        merchant_id: UUID,
        amount_minor: int,
        currency: str,
        payment_method: str,
        device_id: UUID,
        network_identity_id: UUID,
        country_code: str,
        status: str,
        occurred_at: datetime,
        available_at: datetime,
    ) -> Transaction:
        PaymentService.get_customer(db, customer_id)
        PaymentService.get_merchant(db, merchant_id)
        PaymentService.get_device(db, device_id)
        PaymentService.get_network_identity(db, network_identity_id)

        transaction = Transaction(
            customer_id=customer_id,
            merchant_id=merchant_id,
            amount_minor=amount_minor,
            currency=currency.upper(),
            payment_method=payment_method,
            device_id=device_id,
            network_identity_id=network_identity_id,
            country_code=country_code.upper(),
            status=status,
            occurred_at=occurred_at,
            available_at=available_at,
        )
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction

    @staticmethod
    def get_transaction(db: Session, transaction_id: UUID) -> Transaction:
        transaction = db.get(Transaction, transaction_id)
        if transaction is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found",
            )
        return transaction
