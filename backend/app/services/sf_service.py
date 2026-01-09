"""
SuccessFactors API integration service
"""
import requests
import base64
from typing import Dict, Optional, Any
import os
from dotenv import load_dotenv

load_dotenv()


class SuccessFactorsService:
    """Service for interacting with SuccessFactors APIs"""
    
    def __init__(self):
        self.base_url = os.getenv("SF_BASE_URL", "https://api.successfactors.com")
        self.api_version = os.getenv("SF_API_VERSION", "v2")
    
    async def validate_credentials(
        self,
        company_id: str,
        username: str,
        password: str,
        application: str
    ) -> bool:
        """
        Validate SuccessFactors credentials
        Uses OAuth 2.0 or Basic Auth depending on SF configuration
        """
        try:
            # SuccessFactors OAuth 2.0 authentication
            auth_url = f"{self.base_url}/oauth/token"
            
            # Basic authentication for token request
            credentials = f"{username}@{company_id}:{password}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            
            headers = {
                "Authorization": f"Basic {encoded_credentials}",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            
            data = {
                "grant_type": "client_credentials",
                "client_id": username,
                "client_secret": password
            }
            
            response = requests.post(auth_url, headers=headers, data=data, timeout=10)
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get("access_token")
                return True
            else:
                return False
                
        except Exception as e:
            print(f"Error validating credentials: {str(e)}")
            return False
    
    async def get_access_token(
        self,
        company_id: str,
        username: str,
        password: str
    ) -> Optional[str]:
        """Get OAuth access token"""
        try:
            auth_url = f"{self.base_url}/oauth/token"
            credentials = f"{username}@{company_id}:{password}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            
            headers = {
                "Authorization": f"Basic {encoded_credentials}",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            
            data = {"grant_type": "client_credentials"}
            response = requests.post(auth_url, headers=headers, data=data, timeout=10)
            
            if response.status_code == 200:
                return response.json().get("access_token")
            return None
        except Exception as e:
            print(f"Error getting access token: {str(e)}")
            return None
    
    async def implement_configuration(
        self,
        connection: Any,
        configuration_data: Dict,
        workbook_version: Any
    ) -> Dict:
        """
        Implement configuration changes to SuccessFactors
        This is where the actual SF API calls are made
        """
        try:
            # Get access token
            token = await self.get_access_token(
                company_id=connection.company_id,
                username=connection.username,
                password=connection.password_encrypted  # Should be decrypted
            )
            
            if not token:
                raise Exception("Failed to authenticate with SuccessFactors")
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            changes_applied = 0
            errors = []
            
            # Process each configuration item
            for config_item in configuration_data.get("configurations", []):
                try:
                    # Determine the SF API endpoint based on configuration type
                    endpoint = self._get_endpoint_for_config(config_item.get("type"))
                    
                    # Make API call to SF
                    response = requests.post(
                        f"{self.base_url}/{self.api_version}/{endpoint}",
                        headers=headers,
                        json=config_item.get("data"),
                        timeout=30
                    )
                    
                    if response.status_code in [200, 201]:
                        changes_applied += 1
                    else:
                        errors.append({
                            "config_item": config_item.get("id"),
                            "error": response.text
                        })
                except Exception as e:
                    errors.append({
                        "config_item": config_item.get("id"),
                        "error": str(e)
                    })
            
            return {
                "id": f"impl_{workbook_version.id}",
                "changes_count": changes_applied,
                "errors": errors,
                "status": "success" if not errors else "partial"
            }
            
        except Exception as e:
            return {
                "id": f"impl_{workbook_version.id}",
                "changes_count": 0,
                "errors": [str(e)],
                "status": "failed"
            }
    
    def _get_endpoint_for_config(self, config_type: str) -> str:
        """Map configuration type to SF API endpoint"""
        endpoint_map = {
            "user": "User",
            "position": "Position",
            "job": "Job",
            "department": "Department",
            "pay_grade": "PayGrade",
            "compensation": "Compensation",
            "permission": "Permission",
            "workflow": "Workflow",
            "form_template": "FormTemplate",
            "rating_scale": "RatingScale"
        }
        return endpoint_map.get(config_type, "GenericObject")
