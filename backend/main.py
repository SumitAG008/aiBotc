"""
SuccessFactors Configuration Bot - Main Application
This bot helps automate SuccessFactors configuration using workbook-based approach
"""
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import uvicorn
from typing import List, Optional
import os
from dotenv import load_dotenv

from app.database import get_db, init_db
from app.models import SFConnection, Workbook, WorkbookVersion
from app.schemas import (
    SFConnectionCreate, SFConnectionResponse,
    WorkbookCreate, WorkbookResponse,
    WorkbookVersionResponse,
    LoginRequest, LoginResponse
)
from app.services.sf_service import SuccessFactorsService
from app.services.workbook_service import WorkbookService
from app.services.version_control import VersionControlService
from app.services.ai_bot import AIBotService
from app.auth import verify_token, create_access_token

load_dotenv()

app = FastAPI(
    title="SuccessFactors Configuration Bot",
    description="AI-powered bot for automating SuccessFactors configuration management",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()


@app.get("/")
async def root():
    return {
        "message": "SuccessFactors Configuration Bot API",
        "version": "1.0.0",
        "status": "operational"
    }


@app.post("/api/auth/login", response_model=LoginResponse)
async def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate with SuccessFactors and get access token
    """
    try:
        sf_service = SuccessFactorsService()
        # Validate SF credentials
        is_valid = await sf_service.validate_credentials(
            company_id=credentials.company_id,
            username=credentials.username,
            password=credentials.password,
            application=credentials.application
        )
        
        if not is_valid:
            raise HTTPException(status_code=401, detail="Invalid SuccessFactors credentials")
        
        # Create or update SF connection
        sf_connection = db.query(SFConnection).filter(
            SFConnection.company_id == credentials.company_id,
            SFConnection.username == credentials.username
        ).first()
        
        if not sf_connection:
            sf_connection = SFConnection(
                company_id=credentials.company_id,
                username=credentials.username,
                application=credentials.application
            )
            db.add(sf_connection)
        else:
            sf_connection.application = credentials.application
        
        db.commit()
        db.refresh(sf_connection)
        
        # Generate JWT token
        token = create_access_token(data={"sub": sf_connection.id})
        
        return LoginResponse(
            access_token=token,
            token_type="bearer",
            connection_id=sf_connection.id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/connections", response_model=SFConnectionResponse)
async def create_connection(
    connection: SFConnectionCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Create a new SuccessFactors connection"""
    token_data = verify_token(credentials.credentials)
    # Implementation for creating connection
    pass


@app.get("/api/workbooks", response_model=List[WorkbookResponse])
async def get_workbooks(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get all workbooks"""
    token_data = verify_token(credentials.credentials)
    workbooks = db.query(Workbook).all()
    return workbooks


@app.post("/api/workbooks/upload")
async def upload_workbook(
    file: UploadFile = File(...),
    description: Optional[str] = None,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Upload a workbook for SuccessFactors configuration
    Supports Excel (.xlsx) and CSV files
    """
    token_data = verify_token(credentials.credentials)
    
    try:
        workbook_service = WorkbookService()
        workbook = await workbook_service.process_upload(
            file=file,
            user_id=token_data.get("sub"),
            description=description,
            db=db
        )
        return {"message": "Workbook uploaded successfully", "workbook_id": workbook.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/workbooks/{workbook_id}/implement")
async def implement_workbook(
    workbook_id: int,
    version_id: Optional[int] = None,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Implement workbook configuration to SuccessFactors
    Uses AI bot to analyze and apply configurations
    """
    token_data = verify_token(credentials.credentials)
    
    try:
        workbook = db.query(Workbook).filter(Workbook.id == workbook_id).first()
        if not workbook:
            raise HTTPException(status_code=404, detail="Workbook not found")
        
        # Get SF connection
        sf_connection = db.query(SFConnection).filter(
            SFConnection.id == workbook.connection_id
        ).first()
        
        if not sf_connection:
            raise HTTPException(status_code=404, detail="SF Connection not found")
        
        # Initialize services
        sf_service = SuccessFactorsService()
        ai_bot = AIBotService()
        workbook_service = WorkbookService()
        
        # Get workbook version
        if version_id:
            version = db.query(WorkbookVersion).filter(
                WorkbookVersion.id == version_id
            ).first()
        else:
            version = db.query(WorkbookVersion).filter(
                WorkbookVersion.workbook_id == workbook_id
            ).order_by(WorkbookVersion.version_number.desc()).first()
        
        if not version:
            raise HTTPException(status_code=404, detail="Workbook version not found")
        
        # AI bot analyzes the workbook
        analysis = await ai_bot.analyze_workbook(version.file_path)
        
        # Implement configuration
        implementation_result = await sf_service.implement_configuration(
            connection=sf_connection,
            configuration_data=analysis,
            workbook_version=version
        )
        
        return {
            "message": "Configuration implemented successfully",
            "implementation_id": implementation_result.get("id"),
            "changes_applied": implementation_result.get("changes_count", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/workbooks/{workbook_id}/versions", response_model=List[WorkbookVersionResponse])
async def get_workbook_versions(
    workbook_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get all versions of a workbook"""
    token_data = verify_token(credentials.credentials)
    versions = db.query(WorkbookVersion).filter(
        WorkbookVersion.workbook_id == workbook_id
    ).order_by(WorkbookVersion.version_number.desc()).all()
    return versions


@app.post("/api/workbooks/{workbook_id}/analyze")
async def analyze_workbook(
    workbook_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Use AI bot to analyze workbook and provide recommendations
    """
    token_data = verify_token(credentials.credentials)
    
    try:
        workbook = db.query(Workbook).filter(Workbook.id == workbook_id).first()
        if not workbook:
            raise HTTPException(status_code=404, detail="Workbook not found")
        
        version = db.query(WorkbookVersion).filter(
            WorkbookVersion.workbook_id == workbook_id
        ).order_by(WorkbookVersion.version_number.desc()).first()
        
        if not version:
            raise HTTPException(status_code=404, detail="No version found")
        
        ai_bot = AIBotService()
        analysis = await ai_bot.analyze_workbook(version.file_path)
        
        return {
            "workbook_id": workbook_id,
            "analysis": analysis,
            "recommendations": analysis.get("recommendations", []),
            "estimated_changes": analysis.get("estimated_changes", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
