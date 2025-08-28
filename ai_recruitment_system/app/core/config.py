"""
Configuration management for the AI Recruitment System.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration class."""
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # Application Configuration
    APP_TITLE: str = "AI Recruitment System"
    APP_ICON: str = "🤖"
    APP_LAYOUT: str = "wide"
    
    # File Upload Configuration
    ALLOWED_FILE_TYPES: list = ['pdf', 'docx', 'txt']
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate that required configuration is present."""
        if not cls.OPENAI_API_KEY or cls.OPENAI_API_KEY == "your_openai_api_key_here":
            return False
        return True
    
    @classmethod
    def get_error_message(cls) -> Optional[str]:
        """Get error message if configuration is invalid."""
        if not cls.validate_config():
            return "❌ Please set your OPENAI_API_KEY in the .env file"
        return None
