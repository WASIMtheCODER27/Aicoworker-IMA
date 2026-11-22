"""Learning Roadmap Agent: Generates phased learning schedules and portfolio capstone projects."""
import json
from typing import Dict, Any, Optional
from agents.base_agent import BaseAgent
from services.gemini_service import GeminiService
from services.fallback_data import generate_fallback_career_data

class LearningRoadmapAgent(BaseAgent):
    """Creates realistic, phased timelines, weekly milestones, and portfolio project suggestions."""

    def __init__(self, gemini_service: Optional[GeminiService] = None):
        super().__init__(
            name="Learning Roadmap Agent",
            role="Curriculum Architect & Technical Mentor",
            gemini_service=gemini_service
        )

    @property
    def system_instruction(self) -> str:
        return (
            "You are the Learning Roadmap Specialist in AI CareerPilot. "
            "You design high-efficiency, personalized technical learning roadmaps. "
            "You calculate realistic schedules based on the candidate's available daily hours, "
            "structure learning into 4 logical progressive phases with concrete weekly milestones, "
            "and propose 2 industry-ready portfolio projects with resume bullet examples. "
            "You MUST respond ONLY with valid JSON."
        )

    def build_prompt(self, context: Dict[str, Any]) -> str:
        profile = context.get("profile", {})
        target_role = profile.get("target_role", "Software Engineer")
        hours_per_day = profile.get("hours_per_day", 2.0)
        gap_analysis = context.get("skill_gap_analysis", {})
        missing_skills = [s.get("skill", "") for s in gap_analysis.get("prioritized_missing_skills", [])]

        weekly_hours = round(float(hours_per_day) * 7, 1)

        return f"""
Create a personalized 4-phase learning roadmap for {target_role}.

STUDENT PARAMETERS:
- Target Role: {target_role}
- Available Hours Per Day: {hours_per_day} ({weekly_hours} hours/week)
- Skills to Acquire: {", ".join(missing_skills)}
- Current Skills: {", ".join(profile.get("current_skills", []))}
- Experience Level: {profile.get("experience_level", "Entry-level")}

OUTPUT FORMAT REQUIRED (Strict JSON):
{{
  "learning_roadmap": {{
    "total_estimated_weeks": 10,
    "weekly_hours": {weekly_hours},
    "phases": [
      {{
        "phase_title": "Phase 1: Foundations & Core Deficits",
        "duration": "Weeks 1 - 3",
        "weekly_hours": {weekly_hours},
        "focus_areas": ["Specific topic 1", "Specific topic 2", "Specific topic 3"],
        "milestone": "Measurable deliverable or project milestone"
      }},
      {{
        "phase_title": "Phase 2: Architecture & Scalability",
        "duration": "Weeks 4 - 6",
        "weekly_hours": {weekly_hours},
        "focus_areas": ["Specific topic 1", "Specific topic 2"],
        "milestone": "Measurable deliverable"
      }},
      {{
        "phase_title": "Phase 3: Production Tooling & Automation",
        "duration": "Weeks 7 - 8",
        "weekly_hours": {weekly_hours},
        "focus_areas": ["Specific topic 1", "Specific topic 2"],
        "milestone": "Measurable deliverable"
      }},
      {{
        "phase_title": "Phase 4: Capstone Deployment & Polish",
        "duration": "Weeks 9 - 10",
        "weekly_hours": {weekly_hours},
        "focus_areas": ["Specific topic 1", "Specific topic 2"],
        "milestone": "Live published showcase deliverable"
      }}
    ]
  }},
  "suggested_projects": [
    {{
      "title": "Full-Stack / Core {target_role} Capstone Service",
      "difficulty": "Intermediate to Advanced",
      "tech_stack": ["Tech1", "Tech2", "Tech3", "Tech4"],
      "description": "Comprehensive 2-sentence description of what this project does and why it impresses recruiters.",
      "resume_bullet": "Sample resume bullet showing action verb, scope, and metric impact."
    }},
    {{
      "title": "Supporting Real-Time Tool or Library",
      "difficulty": "Intermediate",
      "tech_stack": ["Tech1", "Tech2", "Tech3"],
      "description": "Description of the second portfolio project.",
      "resume_bullet": "Sample resume bullet for this project."
    }}
  ]
}}
"""

    def get_fallback(self, context: Dict[str, Any]) -> Dict[str, Any]:
        profile = context.get("profile", {})
        fb = generate_fallback_career_data(profile)
        return {
            "learning_roadmap": fb["learning_roadmap"],
            "suggested_projects": fb["suggested_projects"]
        }
