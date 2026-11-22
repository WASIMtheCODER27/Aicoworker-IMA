import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

class Config:
    """Application configuration."""
    SECRET_KEY = os.getenv("SECRET_KEY", "careerpilot-dev-secret-key-change-in-production")
    
    # Gemini Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    
    # Upload Settings
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 5 * 1024 * 1024))  # 5 MB
    ALLOWED_EXTENSIONS = {"pdf", "txt", "md"}
    UPLOAD_FOLDER = BASE_DIR / "temp_uploads"
    
    # Server Settings
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "t")
    PORT = int(os.getenv("PORT", 5000))
    HOST = os.getenv("HOST", "127.0.0.1")
    
    # AI Execution Settings
    TIMEOUT_SECONDS = int(os.getenv("TIMEOUT_SECONDS", 45))
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", 2))
