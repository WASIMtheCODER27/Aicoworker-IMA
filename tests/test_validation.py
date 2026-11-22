"""Tests for input and file validation logic."""
import io
import pytest
from werkzeug.datastructures import FileStorage
from services.validator import validate_profile_input, validate_uploaded_file, sanitize_string

def test_sanitize_string():
    """Verify null bytes, control characters, and excess whitespace are stripped."""
    raw = "  Hello \x00 World \x1F!  "
    sanitized = sanitize_string(raw, max_len=50)
    assert sanitized == "Hello World !"
    assert "\x00" not in sanitized
    assert "\x1F" not in sanitized

def test_validate_profile_valid():
    """Verify valid payload passes validation and is sanitized."""
    payload = {
        "name": "Jane Doe",
        "education": "Bachelor of Science",
        "degree": "Computer Science",
        "target_role": "Backend Engineer",
        "current_skills": ["Python", "Django", "PostgreSQL"],
        "experience_level": "Entry-level",
        "hours_per_day": 3.0,
        "career_goals": "Build scalable APIs"
    }
    is_valid, err, sanitized = validate_profile_input(payload)
    assert is_valid is True
    assert err is None
    assert sanitized["name"] == "Jane Doe"
    assert sanitized["target_role"] == "Backend Engineer"
    assert sanitized["hours_per_day"] == 3.0
    assert len(sanitized["current_skills"]) == 3

def test_validate_profile_missing_education():
    """Verify missing education triggers error."""
    payload = {
        "education": "",
        "target_role": "Data Scientist",
        "current_skills": "Python, SQL"
    }
    is_valid, err, _ = validate_profile_input(payload)
    assert is_valid is False
    assert "Education" in err

def test_validate_profile_missing_target_role():
    """Verify missing target role triggers error."""
    payload = {
        "education": "B.Tech",
        "target_role": "",
        "current_skills": "Python"
    }
    is_valid, err, _ = validate_profile_input(payload)
    assert is_valid is False
    assert "Target career role is required" in err

def test_validate_profile_missing_skills():
    """Verify empty skills triggers error."""
    payload = {
        "education": "B.Tech",
        "target_role": "DevOps Engineer",
        "current_skills": []
    }
    is_valid, err, _ = validate_profile_input(payload)
    assert is_valid is False
    assert "At least one current skill" in err

def test_validate_profile_invalid_hours():
    """Verify negative or excessive hours triggers error."""
    payload = {
        "education": "B.Tech",
        "target_role": "DevOps Engineer",
        "current_skills": "Docker",
        "hours_per_day": 25
    }
    is_valid, err, _ = validate_profile_input(payload)
    assert is_valid is False
    assert "between 0.5 and 16" in err

def test_validate_uploaded_file_valid_pdf():
    """Verify valid PDF file is accepted."""
    file = FileStorage(
        stream=io.BytesIO(b"%PDF-1.4 test content"),
        filename="resume.pdf",
        content_type="application/pdf"
    )
    is_valid, err, ext = validate_uploaded_file(file)
    assert is_valid is True
    assert err is None
    assert ext == "pdf"

def test_validate_uploaded_file_invalid_extension():
    """Verify unapproved extensions are rejected."""
    file = FileStorage(
        stream=io.BytesIO(b"binary executable"),
        filename="malicious.exe",
        content_type="application/octet-stream"
    )
    is_valid, err, _ = validate_uploaded_file(file)
    assert is_valid is False
    assert "not supported" in err

def test_validate_uploaded_file_empty_file():
    """Verify 0-byte file is rejected."""
    file = FileStorage(
        stream=io.BytesIO(b""),
        filename="empty.txt",
        content_type="text/plain"
    )
    is_valid, err, _ = validate_uploaded_file(file)
    assert is_valid is False
    assert "empty" in err.lower()
