"""Resume Analyzer Agent: Evaluates resume content, ATS compatibility, bullet points, and structure."""
import json
from typing import Dict, Any, Optional
from agents.base_agent import BaseAgent
from services.gemini_service import GeminiService
from services.fallback_data import generate_fallback_career_data

class ResumeAnalyzerAgent(BaseAgent):
    """Assesses resume content, ATS score, missing sections, and actionable improvements."""

    def __init__(self, gemini_service: Optional[GeminiService] = None):
        super().__init__(
            name="Resume Analyzer Agent",
            role="ATS Specialist & Technical Recruiter",
            gemini_service=gemini_service
        )

    @property
    def system_instruction(self) -> str:
        return (
            "You are the Resume Analyzer Specialist in AI CareerPilot. "
            "You review resumes like a senior technical recruiter and ATS auditor. "
            "You score ATS compatibility (0-100), identify quantifiable strengths, "
            "uncover vague or weak phrasing, pinpoint missing essential sections, "
            "and suggest high-impact keyword and formatting improvements. "
            "You MUST respond ONLY with valid JSON."
        )

    def build_prompt(self, context: Dict[str, Any]) -> str:
        profile = context.get("profile", {})
        has_resume = bool(context.get("has_resume", False))
        resume_text = context.get("resume_text", "")
        profile_insights = context.get("profile_analysis", {})

        return f"""
Analyze the candidate's resume relative to their target role.

TARGET ROLE: {profile.get("target_role", "Software Engineer")}
EDUCATION: {profile.get("education", "N/A")}
DECLARED SKILLS: {", ".join(profile.get("current_skills", []))}
HAS RESUME FILE: {"Yes" if has_resume else "No"}

RESUME TEXT CONTENT:
\"\"\"
{resume_text if has_resume else "No file uploaded. Candidate filled profile inputs manually."}
\"\"\"

OUTPUT FORMAT REQUIRED (Strict JSON):
{{
  "resume_analysis": {{
    "has_resume": {str(has_resume).lower()},
    "ats_compatibility_score": {78 if has_resume else 0},
    "strengths": [
      "2-3 specific resume strengths (e.g. good tech stack representation, clean layout)"
    ],
    "weak_areas": [
      "2-3 weak areas (e.g. lack of quantified impact metrics, passive verbs)"
    ],
    "missing_sections": [
      "2-3 missing or underspecified elements (e.g. GitHub/portfolio links, metrics, certifications)"
    ],
    "ats_recommendations": [
      "3 concrete recommendations to pass automated applicant tracking systems"
    ]
  }}
}}
"""

    def get_fallback(self, context: Dict[str, Any]) -> Dict[str, Any]:
        profile = context.get("profile", {})
        has_resume = bool(context.get("has_resume", False))
        fb = generate_fallback_career_data(profile, has_resume=has_resume)
        return {
            "resume_analysis": fb["resume_analysis"]
        }
