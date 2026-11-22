"""Profile Analysis Agent: Evaluates user profile, background, skills, and aspirations."""
import json
from typing import Dict, Any, Optional
from agents.base_agent import BaseAgent
from services.gemini_service import GeminiService
from services.fallback_data import generate_fallback_career_data

class ProfileAnalysisAgent(BaseAgent):
    """Understands education, skills, experience, interests, and career goals."""

    def __init__(self, gemini_service: Optional[GeminiService] = None):
        super().__init__(
            name="Profile Analysis Agent",
            role="Technical Career Strategist & Profile Evaluator",
            gemini_service=gemini_service
        )

    @property
    def system_instruction(self) -> str:
        return (
            "You are the Profile Analysis Specialist in AI CareerPilot. "
            "Your responsibility is to analyze a candidate's educational background, declared skills, "
            "experience level, career goals, and daily time commitment. "
            "You evaluate their technical standing, calculate an initial readiness score (0-100), "
            "and identify key strengths and primary growth areas. "
            "You MUST respond ONLY with valid JSON matching the requested structure."
        )

    def build_prompt(self, context: Dict[str, Any]) -> str:
        profile = context.get("profile", {})
        has_resume = bool(context.get("has_resume", False))
        resume_snippet = context.get("resume_text", "")[:1000]

        return f"""
Analyze the candidate profile below and generate an objective evaluation.

CANDIDATE DATA:
- Name: {profile.get("name", "Candidate")}
- Education: {profile.get("education", "N/A")}
- Degree: {profile.get("degree", "N/A")}
- Year of Study: {profile.get("year_of_study", "N/A")}
- Target Role: {profile.get("target_role", "Software Engineer")}
- Experience Level: {profile.get("experience_level", "Entry-level")}
- Current Skills: {", ".join(profile.get("current_skills", []))}
- Interests: {profile.get("interests", "N/A")}
- Career Goals: {profile.get("career_goals", "N/A")}
- Hours Per Day Available: {profile.get("hours_per_day", 2)}
- Resume Uploaded: {"Yes" if has_resume else "No"}
{"- Resume Preview: " + resume_snippet if has_resume else ""}

OUTPUT FORMAT REQUIRED (Strict JSON):
{{
  "candidate_summary": {{
    "name": "{profile.get('name', 'Candidate')}",
    "target_role": "{profile.get('target_role', 'Software Engineer')}",
    "domain_category": "e.g. Full-Stack Web Development, Data Science, DevOps",
    "experience_level": "{profile.get('experience_level', 'Entry-level')}",
    "education": "{profile.get('education', 'N/A')}",
    "daily_learning_commitment": "{profile.get('hours_per_day', 2)} hours/day",
    "overall_readiness_score": 75,
    "readiness_summary": "Comprehensive 2-sentence executive summary of the candidate's career readiness."
  }},
  "profile_analysis": {{
    "key_strengths": ["List of 3-4 specific technical and soft strengths"],
    "growth_areas": ["List of 3 primary growth areas or blindspots"],
    "career_trajectory": "Concise paragraph detailing expected career evolution over the next 1-2 years."
  }}
}}
"""

    def get_fallback(self, context: Dict[str, Any]) -> Dict[str, Any]:
        profile = context.get("profile", {})
        has_resume = bool(context.get("has_resume", False))
        fb = generate_fallback_career_data(profile, has_resume=has_resume)
        return {
            "candidate_summary": fb["candidate_summary"],
            "profile_analysis": fb["profile_analysis"]
        }
