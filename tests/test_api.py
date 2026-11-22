"""Tests for API routes and analysis endpoints."""
import io
import json
import pytest
from app import create_app
from config import Config

class TestConfig(Config):
    TESTING = True
    GEMINI_API_KEY = ""

@pytest.fixture
def client():
    app = create_app(TestConfig)
    with app.test_client() as client:
        yield client

def test_analyze_valid_json_payload(client):
    """Verify POST /api/analyze handles JSON requests and returns full report."""
    payload = {
        "name": "Morgan Davis",
        "education": "Master of Science",
        "degree": "Artificial Intelligence",
        "target_role": "Machine Learning Engineer",
        "experience_level": "Entry-level",
        "current_skills": ["Python", "NumPy", "Scikit-Learn", "Git"],
        "hours_per_day": 3.0,
        "interests": "Deep Learning, MLOps",
        "career_goals": "Deploy LLM applications at scale"
    }

    response = client.post(
        "/api/analyze",
        data=json.dumps(payload),
        content_type="application/json"
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    report = data["report"]
    assert report["is_fallback"] is True
    assert "candidate_summary" in report
    assert report["candidate_summary"]["target_role"] == "Machine Learning Engineer"
    assert len(report["career_path_recommendations"]) >= 3
    assert len(report["skill_gap_analysis"]["prioritized_missing_skills"]) > 0

def test_analyze_multipart_with_resume_file(client):
    """Verify POST /api/analyze processes multipart/form-data with resume file."""
    resume_content = b"Morgan Davis\nSoftware Engineer\nSkills: Python, React, PostgreSQL\nExperience: Built microservices."
    
    data = {
        "name": "Morgan Davis",
        "education": "Bachelor's in CS",
        "target_role": "Full Stack Developer",
        "current_skills": "Python, React, PostgreSQL",
        "experience_level": "Entry-level",
        "hours_per_day": "2.5",
        "resume": (io.BytesIO(resume_content), "resume.txt")
    }

    response = client.post(
        "/api/analyze",
        data=data,
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    res_data = response.get_json()
    assert res_data["success"] is True
    report = res_data["report"]
    assert report["resume_analysis"]["has_resume"] is True
    assert report["resume_analysis"]["ats_compatibility_score"] > 0

def test_analyze_missing_required_fields(client):
    """Verify missing target role returns 400 Bad Request."""
    payload = {
        "name": "Anonymous",
        "education": "Computer Science",
        # missing target_role
        "current_skills": ["Python"]
    }

    response = client.post(
        "/api/analyze",
        data=json.dumps(payload),
        content_type="application/json"
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "required" in data["error"].lower()

def test_analyze_invalid_file_type(client):
    """Verify uploading an invalid file extension returns 400 Bad Request."""
    data = {
        "education": "BS in CS",
        "target_role": "Backend Engineer",
        "current_skills": "Python",
        "hours_per_day": "2",
        "resume": (io.BytesIO(b"executable data"), "malicious.exe")
    }

    response = client.post(
        "/api/analyze",
        data=data,
        content_type="multipart/form-data"
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "not supported" in data["error"].lower()

def test_analyze_corrupt_pdf_returns_422(client):
    """Verify corrupted PDF upload returns 422 Unprocessable Entity."""
    corrupt_pdf = b"%PDF-1.4\nBROKEN CONTENT"
    data = {
        "education": "BS in CS",
        "target_role": "Security Analyst",
        "current_skills": "Network Security, Linux",
        "hours_per_day": "2",
        "resume": (io.BytesIO(corrupt_pdf), "corrupt.pdf")
    }

    response = client.post(
        "/api/analyze",
        data=data,
        content_type="multipart/form-data"
    )

    assert response.status_code == 422
    data = response.get_json()
    assert data["success"] is False
    assert "resume processing error" in data["error"].lower()

def test_analyze_mocked_ai_live_response(monkeypatch):
    """Verify live multi-agent execution when Gemini returns mock valid responses."""
    from services.gemini_service import GeminiService

    # Mock client and generate_json_response
    def mock_generate_json(self, prompt, system_instruction=None, temperature=0.2):
        if "Profile Analysis" in str(system_instruction):
            return True, {
                "candidate_summary": {
                    "name": "Mock Candidate",
                    "target_role": "AI Engineer",
                    "domain_category": "Artificial Intelligence",
                    "experience_level": "Entry-level",
                    "education": "BS Computer Science",
                    "daily_learning_commitment": "2.5 hours/day",
                    "overall_readiness_score": 82,
                    "readiness_summary": "Excellent foundation in math and coding."
                },
                "profile_analysis": {
                    "key_strengths": ["Strong Python", "Problem solving"],
                    "growth_areas": ["Model deployment in production"],
                    "career_trajectory": "Fast promotion trajectory"
                }
            }, None
        elif "Resume Analyzer" in str(system_instruction):
            return True, {
                "resume_analysis": {
                    "has_resume": True,
                    "ats_compatibility_score": 85,
                    "strengths": ["Clean layout"],
                    "weak_areas": ["Needs more metrics"],
                    "missing_sections": ["Publications"],
                    "ats_recommendations": ["Include keyword 'PyTorch'"]
                }
            }, None
        elif "Career Path" in str(system_instruction):
            return True, {
                "career_path_recommendations": [
                    {
                        "title": "AI Engineer",
                        "match_score": 88,
                        "demand_level": "Extreme",
                        "salary_range": "$120,000 - $160,000",
                        "fit_reason": "Direct alignment with goals",
                        "entry_requirements": ["Python", "PyTorch"]
                    }
                ]
            }, None
        elif "Skill Gap" in str(system_instruction):
            return True, {
                "skill_gap_analysis": {
                    "current_strengths": ["Python"],
                    "prioritized_missing_skills": [
                        {
                            "skill": "MLOps",
                            "priority": "High",
                            "time_to_learn": "4 weeks",
                            "category": "Deployment",
                            "importance": "Key for production"
                        }
                    ],
                    "competitive_advantage": "Strong CS core"
                }
            }, None
        elif "Learning Roadmap" in str(system_instruction):
            return True, {
                "learning_roadmap": {
                    "total_estimated_weeks": 8,
                    "weekly_hours": 14,
                    "phases": [
                        {
                            "phase_title": "Phase 1: MLOps Foundation",
                            "duration": "Weeks 1-4",
                            "weekly_hours": 14,
                            "focus_areas": ["Docker", "MLflow"],
                            "milestone": "Model API deployed"
                        }
                    ]
                },
                "suggested_projects": [
                    {
                        "title": "LLM Agent Service",
                        "difficulty": "Advanced",
                        "tech_stack": ["FastAPI", "Gemini", "Docker"],
                        "description": "Production LLM service",
                        "resume_bullet": "Built LLM service handling 50 req/s."
                    }
                ]
            }, None
        elif "Interview Preparation" in str(system_instruction):
            return True, {
                "interview_preparation": {
                    "technical_questions": [
                        {
                            "question": "Explain attention mechanism in Transformers.",
                            "focus_area": "Deep Learning",
                            "sample_guidance": "Discuss Q, K, V matrices and softmax scaling.",
                            "key_talking_points": ["Scaled dot-product", "Multi-head attention"]
                        }
                    ],
                    "behavioral_questions": [
                        {
                            "question": "Tell me about a time you handled model drift.",
                            "competency": "Problem Solving",
                            "sample_guidance": "Use STAR framework.",
                            "key_talking_points": ["Detection", "Retraining"]
                        }
                    ],
                    "practice_exercise": "Implement self-attention in 30 minutes."
                },
                "actionable_next_steps": [
                    "Complete Phase 1 Docker course",
                    "Add unit tests to GitHub project"
                ]
            }, None
        return False, None, "Unknown agent instruction"

    monkeypatch.setattr(GeminiService, "is_configured", lambda self: True)
    monkeypatch.setattr(GeminiService, "generate_json_response", mock_generate_json)

    app = create_app(TestConfig)
    with app.test_client() as client:
        payload = {
            "name": "Live Tester",
            "education": "BS in CS",
            "target_role": "AI Engineer",
            "current_skills": ["Python", "PyTorch"],
            "hours_per_day": 2.0
        }
        res = client.post("/api/analyze", data=json.dumps(payload), content_type="application/json")
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        report = data["report"]
        assert report["is_fallback"] is False
        assert "Live Multi-Agent" in report["orchestration_metadata"]["pipeline_mode"]
        assert report["candidate_summary"]["target_role"] == "AI Engineer"
        assert len(report["career_path_recommendations"]) == 1
        assert report["career_path_recommendations"][0]["title"] == "AI Engineer"
