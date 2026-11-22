"""Career Path Agent: Recommends realistic career trajectories, role matches, and entry criteria."""
import json
from typing import Dict, Any, Optional
from agents.base_agent import BaseAgent
from services.gemini_service import GeminiService
from services.fallback_data import generate_fallback_career_data

class CareerPathAgent(BaseAgent):
    """Recommends suitable career roles with match percentages, reasons, and prerequisites."""

    def __init__(self, gemini_service: Optional[GeminiService] = None):
        super().__init__(
            name="Career Path Agent",
            role="Labor Market Analyst & Career Path Architect",
            gemini_service=gemini_service
        )

    @property
    def system_instruction(self) -> str:
        return (
            "You are the Career Path Specialist in AI CareerPilot. "
            "You analyze candidate qualifications, interests, and target roles against current tech industry hiring trends. "
            "You recommend 3 calibrated career paths (including the target role and viable adjacent paths), "
            "providing realistic match scores (0-100), current demand levels, market salary ranges, "
            "reasoning for the match, and concrete entry requirements. "
            "You MUST respond ONLY with valid JSON."
        )

    def build_prompt(self, context: Dict[str, Any]) -> str:
        profile = context.get("profile", {})
        profile_analysis = context.get("profile_analysis", {})
        resume_analysis = context.get("resume_analysis", {})

        return f"""
Analyze the candidate's profile and recommend 3 high-probability career paths.

CANDIDATE CONTEXT:
- Target Role: {profile.get("target_role", "Software Engineer")}
- Current Skills: {", ".join(profile.get("current_skills", []))}
- Education: {profile.get("education", "N/A")}
- Experience Level: {profile.get("experience_level", "Entry-level")}
- Interests: {profile.get("interests", "N/A")}
- Goals: {profile.get("career_goals", "N/A")}

OUTPUT FORMAT REQUIRED (Strict JSON):
{{
  "career_path_recommendations": [
    {{
      "title": "Exact Role Title (e.g. {profile.get('target_role')})",
      "match_score": 85,
      "demand_level": "High / Extreme / Moderate",
      "salary_range": "e.g. $85,000 - $130,000",
      "fit_reason": "2 sentences explaining why this fits their specific profile and skills.",
      "entry_requirements": [
        "Requirement 1",
        "Requirement 2",
        "Requirement 3",
        "Requirement 4"
      ]
    }},
    {{
      "title": "Adjacent High-Potential Role 2",
      "match_score": 75,
      "demand_level": "High",
      "salary_range": "e.g. $90,000 - $140,000",
      "fit_reason": "Why this adjacent role makes strategic sense.",
      "entry_requirements": ["Req 1", "Req 2", "Req 3"]
    }},
    {{
      "title": "Adjacent High-Potential Role 3",
      "match_score": 70,
      "demand_level": "Moderate to High",
      "salary_range": "e.g. $80,000 - $120,000",
      "fit_reason": "Why this alternate route could accelerate their career entry.",
      "entry_requirements": ["Req 1", "Req 2", "Req 3"]
    }}
  ]
}}
"""

    def get_fallback(self, context: Dict[str, Any]) -> Dict[str, Any]:
        profile = context.get("profile", {})
        fb = generate_fallback_career_data(profile)
        return {
            "career_path_recommendations": fb["career_path_recommendations"]
        }
