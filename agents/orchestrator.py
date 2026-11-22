"""Central Multi-Agent Orchestrator for AI CareerPilot."""
import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from agents.profile_agent import ProfileAnalysisAgent
from agents.resume_agent import ResumeAnalyzerAgent
from agents.career_path_agent import CareerPathAgent
from agents.skill_gap_agent import SkillGapAgent
from agents.roadmap_agent import LearningRoadmapAgent
from agents.interview_agent import InterviewPrepAgent
from services.gemini_service import GeminiService
from services.fallback_data import generate_fallback_career_data

logger = logging.getLogger(__name__)

class CareerOrchestrator:
    """
    Coordinates six specialist AI agents in a staged pipeline:
    1. Profile Analysis Agent
    2. Resume Analyzer Agent
    3. Career Path Agent
    4. Skill Gap Agent
    5. Learning Roadmap Agent
    6. Interview Preparation Agent
    
    Passes contextual results between stages and compiles a unified report.
    """

    def __init__(self, gemini_service: Optional[GeminiService] = None):
        self.gemini_service = gemini_service or GeminiService()
        self.profile_agent = ProfileAnalysisAgent(self.gemini_service)
        self.resume_agent = ResumeAnalyzerAgent(self.gemini_service)
        self.career_path_agent = CareerPathAgent(self.gemini_service)
        self.skill_gap_agent = SkillGapAgent(self.gemini_service)
        self.roadmap_agent = LearningRoadmapAgent(self.gemini_service)
        self.interview_agent = InterviewPrepAgent(self.gemini_service)

    def analyze_career(
        self,
        profile: Dict[str, Any],
        resume_text: str = "",
        has_resume: bool = False
    ) -> Dict[str, Any]:
        """
        Execute full multi-agent career analysis.
        Returns unified report dictionary.
        """
        is_live_ai = self.gemini_service.is_configured()

        # If Gemini is not configured, directly deliver the rich offline fallback report
        if not is_live_ai:
            logger.info("Gemini API key is not configured. Running offline heuristic fallback.")
            report = generate_fallback_career_data(profile, has_resume=has_resume, resume_text=resume_text)
            report["orchestration_metadata"] = {
                "pipeline_mode": "Offline Heuristic Fallback",
                "is_fallback": True,
                "model": "None (Demo Mode)",
                "agents_executed": [
                    "Profile Analysis Agent (Heuristic)",
                    "Resume Analyzer Agent (Heuristic)",
                    "Career Path Agent (Heuristic)",
                    "Skill Gap Agent (Heuristic)",
                    "Learning Roadmap Agent (Heuristic)",
                    "Interview Preparation Agent (Heuristic)"
                ],
                "generated_at": datetime.now(timezone.utc).isoformat()
            }
            return report

        # Staged Multi-Agent Pipeline
        context: Dict[str, Any] = {
            "profile": profile,
            "has_resume": has_resume,
            "resume_text": resume_text
        }
        
        executed_agents: List[Dict[str, str]] = []

        try:
            # 1. Profile Analysis Agent
            logger.info("Executing Agent 1: Profile Analysis Agent")
            profile_out = self.profile_agent.run(context)
            context["candidate_summary"] = profile_out.get("candidate_summary", {})
            context["profile_analysis"] = profile_out.get("profile_analysis", {})
            executed_agents.append({"name": self.profile_agent.name, "status": "COMPLETED"})

            # 2. Resume Analyzer Agent
            logger.info("Executing Agent 2: Resume Analyzer Agent")
            resume_out = self.resume_agent.run(context)
            context["resume_analysis"] = resume_out.get("resume_analysis", {})
            executed_agents.append({"name": self.resume_agent.name, "status": "COMPLETED"})

            # 3. Career Path Agent
            logger.info("Executing Agent 3: Career Path Agent")
            path_out = self.career_path_agent.run(context)
            context["career_path_recommendations"] = path_out.get("career_path_recommendations", [])
            executed_agents.append({"name": self.career_path_agent.name, "status": "COMPLETED"})

            # 4. Skill Gap Agent
            logger.info("Executing Agent 4: Skill Gap Agent")
            gap_out = self.skill_gap_agent.run(context)
            context["skill_gap_analysis"] = gap_out.get("skill_gap_analysis", {})
            executed_agents.append({"name": self.skill_gap_agent.name, "status": "COMPLETED"})

            # 5. Learning Roadmap Agent
            logger.info("Executing Agent 5: Learning Roadmap Agent")
            roadmap_out = self.roadmap_agent.run(context)
            context["learning_roadmap"] = roadmap_out.get("learning_roadmap", {})
            context["suggested_projects"] = roadmap_out.get("suggested_projects", [])
            executed_agents.append({"name": self.roadmap_agent.name, "status": "COMPLETED"})

            # 6. Interview Preparation Agent
            logger.info("Executing Agent 6: Interview Preparation Agent")
            interview_out = self.interview_agent.run(context)
            context["interview_preparation"] = interview_out.get("interview_preparation", {})
            context["actionable_next_steps"] = interview_out.get("actionable_next_steps", [])
            executed_agents.append({"name": self.interview_agent.name, "status": "COMPLETED"})

            # Harmonize Composite Readiness Score
            readiness = context["candidate_summary"].get("overall_readiness_score", 70)
            if has_resume:
                ats_score = context["resume_analysis"].get("ats_compatibility_score", 70)
                # Weighted composite: 60% profile skills readiness, 40% ATS resume strength
                composite_score = int(round(readiness * 0.6 + ats_score * 0.4))
                context["candidate_summary"]["overall_readiness_score"] = composite_score

            unified_report = {
                "is_fallback": False,
                "fallback_notice": None,
                "candidate_summary": context["candidate_summary"],
                "profile_analysis": context["profile_analysis"],
                "resume_analysis": context["resume_analysis"],
                "career_path_recommendations": context["career_path_recommendations"],
                "skill_gap_analysis": context["skill_gap_analysis"],
                "learning_roadmap": context["learning_roadmap"],
                "suggested_projects": context["suggested_projects"],
                "interview_preparation": context["interview_preparation"],
                "actionable_next_steps": context["actionable_next_steps"],
                "orchestration_metadata": {
                    "pipeline_mode": "Live Multi-Agent Gemini Pipeline",
                    "is_fallback": False,
                    "model": self.gemini_service.model,
                    "agents_executed": [a["name"] for a in executed_agents],
                    "generated_at": datetime.now(timezone.utc).isoformat()
                }
            }

            return unified_report

        except Exception as e:
            logger.error(f"Error during agent pipeline execution: {str(e)}. Falling back.")
            fallback_report = generate_fallback_career_data(profile, has_resume=has_resume, resume_text=resume_text)
            fallback_report["is_fallback"] = True
            fallback_report["fallback_notice"] = f"DEMO MODE: Analysis completed via offline fallback due to provider error ({str(e)})."
            fallback_report["orchestration_metadata"] = {
                "pipeline_mode": "Fallback After Execution Error",
                "is_fallback": True,
                "error_details": str(e),
                "model": "Fallback Engine",
                "agents_executed": [a["name"] for a in executed_agents] if executed_agents else ["All Agents Fallback"],
                "generated_at": datetime.now(timezone.utc).isoformat()
            }
            return fallback_report
