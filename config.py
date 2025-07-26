import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration settings for the Financial News Analysis Agent"""
    
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")
    
    # Model Settings
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    DEFAULT_TEMPERATURE = float(os.getenv("DEFAULT_TEMPERATURE", "0.3"))
    DEFAULT_MAX_TOKENS = int(os.getenv("DEFAULT_MAX_TOKENS", "500"))
    
    # Application Settings
    APP_TITLE = "📰 Financial News Analysis Agent"
    APP_DESCRIPTION = "AI-powered financial news analysis using Google Gemini"
    
    # Validation
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present"""
        missing_keys = []
        
        if not cls.GEMINI_API_KEY:
            missing_keys.append("GEMINI_API_KEY")
        if not cls.SERPER_API_KEY:
            missing_keys.append("SERPER_API_KEY")
            
        if missing_keys:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_keys)}\n"
                "Please create a .env file with the required API keys."
            )
        
        return True

# Create global config instance
config = Config() 