"""Interview Preparation Agent: Generates technical & behavioral questions, answer guides, and next steps."""
import json
from typing import Dict, Any, Optional
from agents.base_agent import BaseAgent
from services.gemini_service import GeminiService
from services.fallback_data import generate_fallback_career_data

class InterviewPrepAgent(BaseAgent):
    """Produces role-specific technical questions, behavioral STAR scenarios, and immediate next steps."""

    def __init__(self, gemini_service: Optional[GeminiService] = None):
        super().__init__(
            name="Interview Preparation Agent",
            role="Technical Interview Coach & Bar Raiser",
            gemini_service=gemini_service
        )

    @property
    def system_instruction(self) -> str:
        return (
            "You are the Interview Preparation Specialist in AI CareerPilot. "
            "You prepare candidates to pass demanding technical and behavioral interview loops. "
            "You create 3 technical questions targeting the candidate's specific role and gaps, "
            "2 behavioral questions evaluated using the STAR technique, 1 hands-on practice exercise, "
            "and 5 immediate, actionable next steps. "
            "You MUST respond ONLY with valid JSON."
        )

    def build_prompt(self, context: Dict[str, Any]) -> str:
        profile = context.get("profile", {})
        target_role = profile.get("target_role", "Software Engineer")
        skills = profile.get("current_skills", [])
        gap_analysis = context.get("skill_gap_analysis", {})
        missing_skills = [s.get("skill", "") for s in gap_analysis.get("prioritized_missing_skills", [])]

        return f"""
Prepare interview questions and guidance for a candidate applying for {target_role}.

CANDIDATE CONTEXT:
- Role: {target_role}
- Experience Level: {profile.get("experience_level", "Entry-level")}
- Core Skills: {", ".join(skills)}
- Priority Target Areas: {", ".join(missing_skills)}

OUTPUT FORMAT REQUIRED (Strict JSON):
{{
  "interview_preparation": {{
    "technical_questions": [
      {{
        "question": "Realistic technical interview question testing concepts in {target_role}?",
        "focus_area": "e.g. System Design, Concurrency, Algorithms, Framework Internals",
        "sample_guidance": "Clear explanation of what an excellent candidate response covers.",
        "key_talking_points": ["Point 1", "Point 2", "Point 3"]
      }},
      {{
        "question": "Second technical question testing a practical scenario?",
        "focus_area": "Debugging / Performance / Database",
        "sample_guidance": "Guidance on how to structure the answer.",
        "key_talking_points": ["Point 1", "Point 2", "Point 3"]
      }},
      {{
        "question": "Third technical question testing API or code reliability?",
        "focus_area": "Architecture & Security",
        "sample_guidance": "Guidance on trade-offs and edge cases.",
        "key_talking_points": ["Point 1", "Point 2"]
      }}
    ],
    "behavioral_questions": [
      {{
        "question": "Behavioral question testing teamwork or conflict?",
        "competency": "Collaboration / Conflict Resolution",
        "sample_guidance": "How to structure using the STAR method (Situation, Task, Action, Result).",
        "key_talking_points": ["Talking point 1", "Talking point 2"]
      }},
      {{
        "question": "Behavioral question testing deadline management or failure?",
        "competency": "Adaptability & Ownership",
        "sample_guidance": "How to answer with transparency and learning outcomes.",
        "key_talking_points": ["Talking point 1", "Talking point 2"]
      }}
    ],
    "practice_exercise": "A 45-minute timed mock architectural or coding scenario to practice right now."
  }},
  "actionable_next_steps": [
    "Immediate step 1 to take within 24 hours",
    "Immediate step 2 to take within 48 hours",
    "Step 3 for this week",
    "Step 4 for this week",
    "Step 5 for this month"
  ]
}}
"""

    def get_fallback(self, context: Dict[str, Any]) -> Dict[str, Any]:
        profile = context.get("profile", {})
        fb = generate_fallback_career_data(profile)
        return {
            "interview_preparation": fb["interview_preparation"],
            "actionable_next_steps": fb["actionable_next_steps"]
        }
