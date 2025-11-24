from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from decimal import Decimal
from enum import Enum


class InvoiceStatus(str, Enum):
    """Invoice status enumeration."""
    DRAFT = "draft"
    SENT = "sent"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class InvoiceBase(BaseModel):
    """Base invoice schema."""
    account_id: int
    job_id: int
    invoice_number: str
    description: Optional[str] = None
    amount: Decimal
    tax_amount: Decimal = Decimal("0")
    total_amount: Decimal
    status: InvoiceStatus = InvoiceStatus.DRAFT
    due_date: Optional[datetime] = None
    notes: Optional[str] = None


class InvoiceCreate(InvoiceBase):
    """Schema for creating an invoice."""
    pass


class InvoiceUpdate(BaseModel):
    """Schema for updating an invoice."""
    description: Optional[str] = None
    amount: Optional[Decimal] = None
    tax_amount: Optional[Decimal] = None
    total_amount: Optional[Decimal] = None
    status: Optional[InvoiceStatus] = None
    due_date: Optional[datetime] = None
    paid_date: Optional[datetime] = None
    notes: Optional[str] = None


class Invoice(InvoiceBase):
    """Invoice schema for responses."""
    id: int
    issued_date: datetime
    paid_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
