from __future__ import annotations

import pytest
from sqlalchemy import text

from app.db.session import SessionLocal


@pytest.fixture(autouse=True)
def reset_payment_tables() -> None:
    with SessionLocal() as db:
        db.execute(text("TRUNCATE TABLE transactions, customer_devices, network_identities, devices, merchants, customers RESTART IDENTITY CASCADE"))
        db.commit()
    yield
    with SessionLocal() as db:
        db.execute(text("TRUNCATE TABLE transactions, customer_devices, network_identities, devices, merchants, customers RESTART IDENTITY CASCADE"))
        db.commit()
