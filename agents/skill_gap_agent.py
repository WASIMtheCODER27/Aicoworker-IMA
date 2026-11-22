"""Skill Gap Agent: Benchmarks candidate skills against target industry requirements."""
import json
from typing import Dict, Any, Optional
from agents.base_agent import BaseAgent
from services.gemini_service import GeminiService
from services.fallback_data import generate_fallback_career_data

class SkillGapAgent(BaseAgent):
    """Compares current competencies against market requirements and prioritizes gaps."""

    def __init__(self, gemini_service: Optional[GeminiService] = None):
        super().__init__(
            name="Skill Gap Agent",
            role="Technical Competency Lead & Skills Auditor",
            gemini_service=gemini_service
        )

    @property
    def system_instruction(self) -> str:
        return (
            "You are the Skill Gap Specialist in AI CareerPilot. "
            "You conduct rigorous delta analyses comparing candidate capabilities with target industry hiring standards. "
            "You identify verified strengths, isolate missing or superficial skills, "
            "and prioritize them into High, Medium, or Low urgency with estimated learning times. "
            "You MUST respond ONLY with valid JSON."
        )

    def build_prompt(self, context: Dict[str, Any]) -> str:
        profile = context.get("profile", {})
        target_role = profile.get("target_role", "Software Engineer")
        skills = profile.get("current_skills", [])
        career_paths = context.get("career_path_recommendations", [])

        target_reqs = []
        if career_paths and len(career_paths) > 0:
            target_reqs = career_paths[0].get("entry_requirements", [])

        return f"""
Perform a skill gap audit comparing the candidate's current skills with requirements for {target_role}.

CANDIDATE CURRENT SKILLS: {", ".join(skills)}
TARGET ROLE: {target_role}
EXPERIENCE LEVEL: {profile.get("experience_level", "Entry-level")}
ENTRY REQUIREMENTS DETECTED: {", ".join(target_reqs)}

OUTPUT FORMAT REQUIRED (Strict JSON):
{{
  "skill_gap_analysis": {{
    "current_strengths": {json.dumps(skills)},
    "prioritized_missing_skills": [
      {{
        "skill": "Name of Missing Skill (e.g. Docker & Containers)",
        "priority": "High",
        "time_to_learn": "3-4 weeks",
        "category": "e.g. Infrastructure, Backend, Data",
        "importance": "Why mastering this skill directly unblocks job offers."
      }},
      {{
        "skill": "Name of Missing Skill 2",
        "priority": "High",
        "time_to_learn": "2-3 weeks",
        "category": "Architecture",
        "importance": "Explanation"
      }},
      {{
        "skill": "Name of Missing Skill 3",
        "priority": "Medium",
        "time_to_learn": "3 weeks",
        "category": "Testing/Tooling",
        "importance": "Explanation"
      }},
      {{
        "skill": "Name of Missing Skill 4",
        "priority": "Medium",
        "time_to_learn": "2 weeks",
        "category": "Cloud/DB",
        "importance": "Explanation"
      }}
    ],
    "competitive_advantage": "A strategic observation on how their existing skills plus these additions create a unique market edge."
  }}
}}
"""

    def get_fallback(self, context: Dict[str, Any]) -> Dict[str, Any]:
        profile = context.get("profile", {})
        fb = generate_fallback_career_data(profile)
        return {
            "skill_gap_analysis": fb["skill_gap_analysis"]
        }
