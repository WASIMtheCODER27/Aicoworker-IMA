"""Tests for specialist agents and orchestrator."""
import pytest
from services.gemini_service import GeminiService
from agents.profile_agent import ProfileAnalysisAgent
from agents.resume_agent import ResumeAnalyzerAgent
from agents.career_path_agent import CareerPathAgent
from agents.skill_gap_agent import SkillGapAgent
from agents.roadmap_agent import LearningRoadmapAgent
from agents.interview_agent import InterviewPrepAgent
from agents.orchestrator import CareerOrchestrator

@pytest.fixture
def mock_context():
    return {
        "profile": {
            "name": "Sam Taylor",
            "education": "Bachelor of Technology",
            "degree": "Information Technology",
            "target_role": "Cloud Architect",
            "experience_level": "Entry-level",
            "current_skills": ["Linux", "Python", "Networking", "AWS Basics"],
            "hours_per_day": 2.5,
            "interests": "Cloud Infrastructure, Distributed Systems",
            "career_goals": "Design fault-tolerant multi-region systems"
        },
        "has_resume": True,
        "resume_text": "Sam Taylor - Cloud Engineer with background in Linux and AWS automation."
    }

def test_extract_clean_json_variations():
    """Verify JSON extractor parses markdown fences, bare strings, and partial JSON."""
    service = GeminiService(api_key="")

    # Standard clean JSON
    assert service.extract_clean_json('{"key": "value"}') == {"key": "value"}

    # Markdown block
    fenced = "```json\n{\n  \"role\": \"SRE\"\n}\n```"
    assert service.extract_clean_json(fenced) == {"role": "SRE"}

    # Text before and after json
    embedded = "Here is the result:\n```\n{\"score\": 85}\n```\nHope this helps."
    assert service.extract_clean_json(embedded) == {"score": 85}

    # Invalid JSON
    assert service.extract_clean_json("Not a json string at all") is None

def test_profile_agent_fallback(mock_context):
    """Verify ProfileAnalysisAgent returns required keys in fallback mode."""
    agent = ProfileAnalysisAgent(gemini_service=GeminiService(api_key=""))
    result = agent.run(mock_context)
    assert "candidate_summary" in result
    assert "profile_analysis" in result
    assert result["candidate_summary"]["name"] == "Sam Taylor"
    assert len(result["profile_analysis"]["key_strengths"]) > 0

def test_resume_agent_fallback(mock_context):
    """Verify ResumeAnalyzerAgent assesses resume and calculates ATS score."""
    agent = ResumeAnalyzerAgent(gemini_service=GeminiService(api_key=""))
    result = agent.run(mock_context)
    assert "resume_analysis" in result
    assert result["resume_analysis"]["has_resume"] is True
    assert result["resume_analysis"]["ats_compatibility_score"] > 0
    assert len(result["resume_analysis"]["ats_recommendations"]) > 0

def test_career_path_agent_fallback(mock_context):
    """Verify CareerPathAgent recommends 3 calibrated roles."""
    agent = CareerPathAgent(gemini_service=GeminiService(api_key=""))
    result = agent.run(mock_context)
    assert "career_path_recommendations" in result
    roles = result["career_path_recommendations"]
    assert len(roles) >= 3
    for r in roles:
        assert "title" in r
        assert "match_score" in r
        assert "salary_range" in r

def test_skill_gap_agent_fallback(mock_context):
    """Verify SkillGapAgent identifies and prioritizes missing competencies."""
    agent = SkillGapAgent(gemini_service=GeminiService(api_key=""))
    result = agent.run(mock_context)
    assert "skill_gap_analysis" in result
    gaps = result["skill_gap_analysis"]["prioritized_missing_skills"]
    assert len(gaps) > 0
    for g in gaps:
        assert "skill" in g
        assert "priority" in g
        assert "time_to_learn" in g

def test_roadmap_agent_fallback(mock_context):
    """Verify LearningRoadmapAgent produces phases and capstone projects."""
    agent = LearningRoadmapAgent(gemini_service=GeminiService(api_key=""))
    result = agent.run(mock_context)
    assert "learning_roadmap" in result
    assert "suggested_projects" in result
    assert len(result["learning_roadmap"]["phases"]) >= 4
    assert len(result["suggested_projects"]) >= 2

def test_interview_prep_agent_fallback(mock_context):
    """Verify InterviewPrepAgent provides technical and behavioral questions."""
    agent = InterviewPrepAgent(gemini_service=GeminiService(api_key=""))
    result = agent.run(mock_context)
    assert "interview_preparation" in result
    assert "actionable_next_steps" in result
    prep = result["interview_preparation"]
    assert len(prep["technical_questions"]) >= 3
    assert len(prep["behavioral_questions"]) >= 2
    assert len(result["actionable_next_steps"]) >= 5

def test_orchestrator_complete_pipeline(mock_context):
    """Verify CareerOrchestrator stitches all 6 agents into unified report."""
    orchestrator = CareerOrchestrator(gemini_service=GeminiService(api_key=""))
    report = orchestrator.analyze_career(
        profile=mock_context["profile"],
        resume_text=mock_context["resume_text"],
        has_resume=mock_context["has_resume"]
    )

    assert report is not None
    assert report["is_fallback"] is True
    assert "orchestration_metadata" in report
    assert "candidate_summary" in report
    assert "profile_analysis" in report
    assert "resume_analysis" in report
    assert "career_path_recommendations" in report
    assert "skill_gap_analysis" in report
    assert "learning_roadmap" in report
    assert "suggested_projects" in report
    assert "interview_preparation" in report
    assert "actionable_next_steps" in report
    assert report["candidate_summary"]["overall_readiness_score"] > 0
