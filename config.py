"""
Configuration settings for Board Agent
"""

import os
from typing import Optional

class Config:
    """Configuration class for Board Agent"""
    
    # Google AI Configuration
    GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")
    GEMINI_MODEL: str = "gemini-2.0-flash-thinking-exp-01-21"
    GEMINI_TEMPERATURE: float = 0.2
    
    # Application Settings
    APP_NAME: str = "Board Agent"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Output Settings
    OUTPUT_DIR: str = "output"
    LOGS_DIR: str = "logs"
    
    # Expert Configuration
    EXPERTS = {
        "legal_advisor": {
            "name": "Legal Advisor",
            "focus": "Indian Penal Code compliance and legal risks"
        },
        "ethics_expert": {
            "name": "Ethics Expert", 
            "focus": "Ethical concerns and fairness issues"
        },
        "financial_analyst": {
            "name": "Financial Analyst",
            "focus": "Cost analysis, ROI, and sustainability"
        },
        "technical_analyst": {
            "name": "Technical Analyst",
            "focus": "Feasibility and technical risks"
        }
    }
    
    # Workflow Configuration
    WORKFLOW_SEQUENCE = [
        "technical_analyst",
        "ethics_expert", 
        "legal_advisor",
        "financial_analyst",
        "technical_analyst2",
        "final_verdict"
    ]
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate that required configuration is present"""
        if not cls.GOOGLE_API_KEY:
            print("Warning: GOOGLE_API_KEY not found in environment variables")
            return False
        return True
    
    @classmethod
    def get_model_config(cls) -> dict:
        """Get model configuration for LangChain"""
        return {
            "model": cls.GEMINI_MODEL,
            "temperature": cls.GEMINI_TEMPERATURE
        }
