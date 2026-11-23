import os
import tempfile
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

# Check potential .env file locations
ENV_CANDIDATES = [
    BASE_DIR / ".env",
    BASE_DIR / "Local" / "Aicoworker.env",
    BASE_DIR / "Aicoworker.env",
    BASE_DIR / "Local" / ".env",
    Path.cwd() / ".env",
    Path.cwd() / "Local" / "Aicoworker.env",
]

def load_app_env(override: bool = False) -> bool:
    """Load environment variables from candidate .env files."""
    loaded = False
    for env_path in ENV_CANDIDATES:
        if env_path.is_file():
            load_dotenv(dotenv_path=env_path, override=override)
            loaded = True
    if not loaded:
        load_dotenv(override=override)
    return loaded

# Perform initial load
load_app_env()

class Config:
    """Application configuration."""
    SECRET_KEY = os.getenv("SECRET_KEY", "careerpilot-dev-secret-key-change-in-production")
    
    # Gemini Configuration
    GEMINI_API_KEY = (os.getenv("GEMINI_API_KEY") or "").strip().strip('"').strip("'")
    GEMINI_MODEL = (os.getenv("GEMINI_MODEL") or "gemini-2.5-flash").strip()
    
    # Upload Settings
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 5 * 1024 * 1024))  # 5 MB
    ALLOWED_EXTENSIONS = {"pdf", "txt", "md"}
    # On serverless (Vercel/Lambda), working dir is read-only; use /tmp for uploads
    if os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
        UPLOAD_FOLDER = Path(tempfile.gettempdir()) / "careerpilot_uploads"
    else:
        UPLOAD_FOLDER = BASE_DIR / "temp_uploads"
    
    # Server Settings
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "t")
    PORT = int(os.getenv("PORT", 5000))
    HOST = os.getenv("HOST", "127.0.0.1")
    
    # AI Execution Settings
    TIMEOUT_SECONDS = int(os.getenv("TIMEOUT_SECONDS", 45))
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", 2))
