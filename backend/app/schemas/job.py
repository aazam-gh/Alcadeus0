from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum


class JobStatus(str, Enum):
    """Job status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class JobBase(BaseModel):
    """Base job schema."""
    account_id: int
    title: str
    description: Optional[str] = None
    address: str
    city: str
    state: str
    zip_code: str
    technician_id: Optional[int] = None
    status: JobStatus = JobStatus.PENDING
    scheduled_date: Optional[datetime] = None


class JobCreate(JobBase):
    """Schema for creating a job."""
    pass


class JobUpdate(BaseModel):
    """Schema for updating a job."""
    title: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    technician_id: Optional[int] = None
    status: Optional[JobStatus] = None
    scheduled_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None


class Job(JobBase):
    """Job schema for responses."""
    id: int
    completed_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
