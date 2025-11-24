from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class TechnicianBase(BaseModel):
    """Base technician schema."""
    account_id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    specialization: Optional[str] = None
    license_number: Optional[str] = None
    is_active: bool = True


class TechnicianCreate(TechnicianBase):
    """Schema for creating a technician."""
    pass


class TechnicianUpdate(BaseModel):
    """Schema for updating a technician."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    specialization: Optional[str] = None
    license_number: Optional[str] = None
    is_active: Optional[bool] = None


class Technician(TechnicianBase):
    """Technician schema for responses."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
