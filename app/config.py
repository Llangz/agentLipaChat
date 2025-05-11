import os
from pydantic import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    """Application settings."""
    APP_NAME: str = "LipaChat AI Agents"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # API Keys
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    LIPACHAT_API_KEY: str = os.getenv("LIPACHAT_API_KEY", "")
    
    # Database
    DB_CONNECTION_STRING: str = os.getenv("DB_CONNECTION_STRING", "")
    
    # Anthropic Claude API
    CLAUDE_MODEL: str = "claude-3-5-sonnet-20240620"  # Update as needed
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Agent settings
    MAX_CONVERSATION_HISTORY: int = 10
    DEFAULT_LANGUAGE: str = "en"
    SUPPORTED_LANGUAGES: list = ["en", "sw", "fr"]  # English, Swahili, French
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()