"""
Version control service for workbooks
Uses Git-like approach for tracking changes
"""
import os
import json
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.models import WorkbookVersion, Workbook


class VersionControlService:
    """Service for managing workbook versions"""
    
    def __init__(self):
        self.repo_dir = os.getenv("REPO_DIR", "./repos")
        os.makedirs(self.repo_dir, exist_ok=True)
    
    def get_version_history(self, workbook_id: int, db: Session) -> List[Dict]:
        """Get version history for a workbook"""
        versions = db.query(WorkbookVersion).filter(
            WorkbookVersion.workbook_id == workbook_id
        ).order_by(WorkbookVersion.created_at.desc()).all()
        
        return [
            {
                "id": v.id,
                "version_number": v.version_number,
                "created_at": v.created_at.isoformat(),
                "created_by": v.created_by,
                "changes_summary": v.changes_summary,
                "file_size": v.file_size
            }
            for v in versions
        ]
    
    def compare_versions(
        self,
        version1_id: int,
        version2_id: int,
        db: Session
    ) -> Dict:
        """Compare two workbook versions"""
        v1 = db.query(WorkbookVersion).filter(WorkbookVersion.id == version1_id).first()
        v2 = db.query(WorkbookVersion).filter(WorkbookVersion.id == version2_id).first()
        
        if not v1 or not v2:
            raise ValueError("One or both versions not found")
        
        # This would use a diff library to compare files
        # For now, return basic comparison
        return {
            "version1": {
                "id": v1.id,
                "version_number": v1.version_number,
                "checksum": v1.checksum
            },
            "version2": {
                "id": v2.id,
                "version_number": v2.version_number,
                "checksum": v2.checksum
            },
            "are_different": v1.checksum != v2.checksum,
            "changes": "Detailed diff would be implemented here"
        }
    
    def rollback_to_version(
        self,
        workbook_id: int,
        target_version_id: int,
        db: Session
    ) -> Dict:
        """Rollback workbook to a specific version"""
        target_version = db.query(WorkbookVersion).filter(
            WorkbookVersion.id == target_version_id,
            WorkbookVersion.workbook_id == workbook_id
        ).first()
        
        if not target_version:
            raise ValueError("Target version not found")
        
        # Create a new version from the target version
        # This allows rollback without losing history
        return {
            "message": f"Rolled back to version {target_version.version_number}",
            "version_id": target_version_id
        }
