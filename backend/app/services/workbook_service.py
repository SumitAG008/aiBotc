"""
Workbook processing and management service
"""
import os
import hashlib
import pandas as pd
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import UploadFile
import aiofiles
from datetime import datetime

from app.models import Workbook, WorkbookVersion


class WorkbookService:
    """Service for processing and managing workbooks"""
    
    def __init__(self):
        self.upload_dir = os.getenv("UPLOAD_DIR", "./uploads/workbooks")
        os.makedirs(self.upload_dir, exist_ok=True)
    
    async def process_upload(
        self,
        file: UploadFile,
        user_id: int,
        description: Optional[str],
        db: Session
    ) -> Workbook:
        """Process uploaded workbook file"""
        
        # Read file content
        content = await file.read()
        
        # Calculate checksum
        checksum = hashlib.sha256(content).hexdigest()
        
        # Check if this version already exists
        existing_version = db.query(WorkbookVersion).filter(
            WorkbookVersion.checksum == checksum
        ).first()
        
        if existing_version:
            raise ValueError("This workbook version already exists")
        
        # Save file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(self.upload_dir, filename)
        
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)
        
        # Parse workbook to extract metadata
        workbook_data = await self._parse_workbook(file_path)
        
        # Create workbook record
        workbook = Workbook(
            name=file.filename,
            description=description or workbook_data.get("description", ""),
            created_by=user_id
        )
        db.add(workbook)
        db.flush()
        
        # Create version record
        version_number = self._get_next_version_number(workbook.id, db)
        version = WorkbookVersion(
            workbook_id=workbook.id,
            version_number=version_number,
            file_path=file_path,
            file_size=len(content),
            checksum=checksum,
            changes_summary=workbook_data.get("summary", ""),
            created_by=user_id
        )
        db.add(version)
        db.commit()
        db.refresh(workbook)
        
        return workbook
    
    async def _parse_workbook(self, file_path: str) -> dict:
        """Parse workbook file and extract configuration data"""
        try:
            if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                # Read Excel file
                df = pd.read_excel(file_path, sheet_name=None)
                
                # Extract metadata
                sheets = list(df.keys())
                total_rows = sum(len(sheet_df) for sheet_df in df.values())
                
                return {
                    "type": "excel",
                    "sheets": sheets,
                    "total_rows": total_rows,
                    "summary": f"Excel workbook with {len(sheets)} sheets and {total_rows} total rows"
                }
            elif file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
                return {
                    "type": "csv",
                    "total_rows": len(df),
                    "columns": list(df.columns),
                    "summary": f"CSV file with {len(df)} rows and {len(df.columns)} columns"
                }
            else:
                return {"type": "unknown", "summary": "Unknown file type"}
        except Exception as e:
            return {"type": "error", "summary": f"Error parsing file: {str(e)}"}
    
    def _get_next_version_number(self, workbook_id: int, db: Session) -> str:
        """Get next version number for workbook"""
        last_version = db.query(WorkbookVersion).filter(
            WorkbookVersion.workbook_id == workbook_id
        ).order_by(WorkbookVersion.version_number.desc()).first()
        
        if not last_version:
            return "1.0.0"
        
        # Simple version increment (can be enhanced)
        version_parts = last_version.version_number.split('.')
        if len(version_parts) == 3:
            major, minor, patch = map(int, version_parts)
            patch += 1
            return f"{major}.{minor}.{patch}"
        else:
            return "1.0.0"
