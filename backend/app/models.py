"""
Database models for SuccessFactors Configuration Bot
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class SFConnection(Base):
    """SuccessFactors connection credentials"""
    __tablename__ = "sf_connections"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(String(100), nullable=False, index=True)
    username = Column(String(255), nullable=False)
    password_encrypted = Column(String(500))  # Encrypted password
    application = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    workbooks = relationship("Workbook", back_populates="connection")


class Workbook(Base):
    """Workbook metadata"""
    __tablename__ = "workbooks"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    connection_id = Column(Integer, ForeignKey("sf_connections.id"))
    created_by = Column(Integer)  # User ID
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    connection = relationship("SFConnection", back_populates="workbooks")
    versions = relationship("WorkbookVersion", back_populates="workbook", cascade="all, delete-orphan")


class WorkbookVersion(Base):
    """Workbook version control"""
    __tablename__ = "workbook_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    workbook_id = Column(Integer, ForeignKey("workbooks.id"), nullable=False)
    version_number = Column(String(50), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)
    checksum = Column(String(64))  # SHA256 checksum for version tracking
    changes_summary = Column(Text)
    created_by = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    workbook = relationship("Workbook", back_populates="versions")


class ImplementationLog(Base):
    """Log of configuration implementations"""
    __tablename__ = "implementation_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    workbook_version_id = Column(Integer, ForeignKey("workbook_versions.id"))
    connection_id = Column(Integer, ForeignKey("sf_connections.id"))
    status = Column(String(50))  # success, failed, partial
    changes_applied = Column(Integer, default=0)
    errors = Column(Text)
    implementation_data = Column(Text)  # JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
