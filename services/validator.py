"""Input and file validation for AI CareerPilot."""
import re
from typing import Dict, Any, Tuple, Optional
from werkzeug.datastructures import FileStorage
from config import Config

ALLOWED_EXTENSIONS = Config.ALLOWED_EXTENSIONS
MAX_CONTENT_LENGTH = Config.MAX_CONTENT_LENGTH

VALID_EXPERIENCE_LEVELS = {
    "student", "beginner", "entry-level", "junior", "mid-level", "senior", "career switcher"
}

def sanitize_string(val: Optional[str], max_len: int = 1000) -> str:
    """Strip whitespace, control chars, and normalize spaces."""
    if not val or not isinstance(val, str):
        return ""
    # Strip null bytes and non-printable control chars
    clean = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', val)
    # Normalize excessive spaces
    clean = re.sub(r'[ \t]+', ' ', clean)
    return clean.strip()[:max_len]

def validate_profile_input(data: Dict[str, Any]) -> Tuple[bool, Optional[str], Dict[str, Any]]:
    """
    Validate user profile fields.
    Returns (is_valid, error_message, sanitized_data).
    """
    if not isinstance(data, dict):
        return False, "Invalid payload format. Expected JSON object.", {}

    # Extract & sanitize fields
    name = sanitize_string(data.get("name", ""), max_len=100)
    education = sanitize_string(data.get("education", ""), max_len=120)
    degree = sanitize_string(data.get("degree", ""), max_len=120)
    year_of_study = sanitize_string(data.get("year_of_study", ""), max_len=80)
    target_role = sanitize_string(data.get("target_role", ""), max_len=100)
    experience_level = sanitize_string(data.get("experience_level", ""), max_len=50)
    interests = sanitize_string(data.get("interests", ""), max_len=500)
    career_goals = sanitize_string(data.get("career_goals", ""), max_len=1000)
    location = sanitize_string(data.get("location", ""), max_len=100)
    
    # Process skills
    raw_skills = data.get("current_skills", "")
    if isinstance(raw_skills, list):
        skills = [sanitize_string(s, max_len=60) for s in raw_skills if sanitize_string(s, max_len=60)]
    elif isinstance(raw_skills, str):
        skills = [sanitize_string(s, max_len=60) for s in raw_skills.split(",") if sanitize_string(s, max_len=60)]
    else:
        skills = []

    # Process hours_per_day
    raw_hours = data.get("hours_per_day", 2)
    try:
        hours_per_day = float(raw_hours)
        if hours_per_day <= 0 or hours_per_day > 16:
            return False, "Preferred learning hours must be between 0.5 and 16 hours per day.", {}
    except (ValueError, TypeError):
        return False, "Preferred learning hours must be a valid number.", {}

    # Required field checks
    if not education:
        return False, "Education level is required (e.g. Bachelor's in CS, High School, Bootcamp).", {}
    
    if not target_role:
        return False, "Target career role is required (e.g. Full Stack Developer, Data Scientist).", {}

    if not skills:
        return False, "At least one current skill or technology is required.", {}

    if not experience_level:
        experience_level = "Entry-level"
    elif experience_level.lower() not in VALID_EXPERIENCE_LEVELS:
        # Default gracefully if reasonable string provided
        if len(experience_level) > 50:
            return False, "Experience level is invalid.", {}

    sanitized = {
        "name": name or "Aspiring Professional",
        "education": education,
        "degree": degree,
        "year_of_study": year_of_study,
        "current_skills": skills,
        "target_role": target_role,
        "experience_level": experience_level.title(),
        "hours_per_day": round(hours_per_day, 1),
        "interests": interests,
        "career_goals": career_goals,
        "location": location
    }

    return True, None, sanitized

def validate_uploaded_file(file: Optional[FileStorage]) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Validate uploaded file size, extension, and content type.
    Returns (is_valid, error_message, extension).
    """
    if file is None or file.filename == "":
        return True, None, None  # Resume upload is optional

    filename = file.filename
    if "." not in filename:
        return False, "Uploaded file lacks a valid extension.", None

    ext = filename.rsplit(".", 1)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"File type '.{ext}' is not supported. Allowed formats: PDF, TXT, MD.", None

    # Check file size by seeking
    try:
        file.seek(0, 2)  # Seek to end
        size = file.tell()
        file.seek(0)  # Reset pointer
        if size > MAX_CONTENT_LENGTH:
            max_mb = MAX_CONTENT_LENGTH / (1024 * 1024)
            return False, f"File size exceeds the limit of {max_mb:.0f}MB.", None
        if size == 0:
            return False, "Uploaded file is empty (0 bytes).", None
    except Exception as e:
        return False, f"Failed to check file size: {str(e)}", None

    return True, None, ext
