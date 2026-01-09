"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class LoginRequest(BaseModel):
    company_id: str
    username: str
    password: str
    application: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    connection_id: int


class SFConnectionCreate(BaseModel):
    company_id: str
    username: str
    password: str
    application: str


class SFConnectionResponse(BaseModel):
    id: int
    company_id: str
    username: str
    application: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class WorkbookCreate(BaseModel):
    name: str
    description: Optional[str] = None
    connection_id: int


class WorkbookResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    connection_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class WorkbookVersionResponse(BaseModel):
    id: int
    workbook_id: int
    version_number: str
    file_path: str
    file_size: Optional[int]
    checksum: Optional[str]
    changes_summary: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
