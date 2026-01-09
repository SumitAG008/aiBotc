"""
AI Bot service for intelligent configuration analysis and recommendations
"""
import os
import pandas as pd
from typing import Dict, List, Any
import json
from dotenv import load_dotenv

# For AI integration - can use OpenAI, LangChain, or other AI services
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

load_dotenv()


class AIBotService:
    """AI-powered bot for analyzing and recommending SuccessFactors configurations"""
    
    def __init__(self):
        self.openai_client = None
        if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
            self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    async def analyze_workbook(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze workbook using AI to understand configuration requirements
        """
        try:
            # Read workbook
            if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                df_dict = pd.read_excel(file_path, sheet_name=None)
            elif file_path.endswith('.csv'):
                df_dict = {"Sheet1": pd.read_csv(file_path)}
            else:
                return {"error": "Unsupported file format"}
            
            # Extract configuration patterns
            configurations = []
            recommendations = []
            
            for sheet_name, df in df_dict.items():
                # Analyze each sheet
                sheet_analysis = self._analyze_sheet(df, sheet_name)
                configurations.extend(sheet_analysis.get("configurations", []))
                recommendations.extend(sheet_analysis.get("recommendations", []))
            
            # Use AI for intelligent recommendations if available
            if self.openai_client:
                ai_recommendations = await self._get_ai_recommendations(
                    configurations, file_path
                )
                recommendations.extend(ai_recommendations)
            
            return {
                "configurations": configurations,
                "recommendations": recommendations,
                "estimated_changes": len(configurations),
                "complexity": self._assess_complexity(configurations),
                "risk_level": self._assess_risk(configurations)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _analyze_sheet(self, df: pd.DataFrame, sheet_name: str) -> Dict:
        """Analyze a single sheet for configuration patterns"""
        configurations = []
        recommendations = []
        
        # Detect configuration type based on column names
        columns = [col.lower() for col in df.columns]
        
        if any("user" in col for col in columns) or any("employee" in col for col in columns):
            config_type = "user"
            recommendations.append({
                "type": "user_management",
                "message": "Detected user/employee configuration. Ensure proper role assignments.",
                "priority": "high"
            })
        elif any("position" in col for col in columns):
            config_type = "position"
        elif any("job" in col for col in columns):
            config_type = "job"
        elif any("compensation" in col for col in columns) or any("salary" in col for col in columns):
            config_type = "compensation"
            recommendations.append({
                "type": "compensation",
                "message": "Compensation changes detected. Review approval workflows.",
                "priority": "high"
            })
        else:
            config_type = "generic"
        
        # Process each row as a configuration item
        for idx, row in df.iterrows():
            config_item = {
                "id": f"{sheet_name}_{idx}",
                "type": config_type,
                "sheet": sheet_name,
                "row": idx + 1,
                "data": row.to_dict()
            }
            configurations.append(config_item)
        
        return {
            "configurations": configurations,
            "recommendations": recommendations
        }
    
    async def _get_ai_recommendations(
        self,
        configurations: List[Dict],
        file_path: str
    ) -> List[Dict]:
        """Get AI-powered recommendations"""
        if not self.openai_client:
            return []
        
        try:
            # Prepare prompt for AI
            config_summary = {
                "total_items": len(configurations),
                "types": list(set(c.get("type") for c in configurations))
            }
            
            prompt = f"""
            Analyze this SuccessFactors configuration workbook:
            - Total configuration items: {config_summary['total_items']}
            - Configuration types: {', '.join(config_summary['types'])}
            
            Provide recommendations for:
            1. Best practices for implementation
            2. Potential risks or issues
            3. Optimization suggestions
            4. Required approvals or workflows
            
            Return as JSON array of recommendations.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a SuccessFactors configuration expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Parse AI response
            ai_text = response.choices[0].message.content
            # In production, properly parse JSON response
            return [
                {
                    "type": "ai_recommendation",
                    "message": ai_text,
                    "priority": "medium",
                    "source": "AI Analysis"
                }
            ]
        except Exception as e:
            print(f"AI recommendation error: {str(e)}")
            return []
    
    def _assess_complexity(self, configurations: List[Dict]) -> str:
        """Assess complexity of configuration"""
        count = len(configurations)
        if count < 10:
            return "low"
        elif count < 50:
            return "medium"
        else:
            return "high"
    
    def _assess_risk(self, configurations: List[Dict]) -> str:
        """Assess risk level of configuration"""
        high_risk_types = ["compensation", "permission", "workflow"]
        has_high_risk = any(
            c.get("type") in high_risk_types for c in configurations
        )
        return "high" if has_high_risk else "medium"
