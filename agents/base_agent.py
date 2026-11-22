"""Base Agent class defining interface and common capabilities for all career agents."""
import abc
import logging
from typing import Dict, Any, Optional
from services.gemini_service import GeminiService

logger = logging.getLogger(__name__)

class BaseAgent(abc.ABC):
    """Abstract base class for all AI CareerPilot specialist agents."""

    def __init__(self, name: str, role: str, gemini_service: Optional[GeminiService] = None):
        self.name = name
        self.role = role
        self.gemini_service = gemini_service or GeminiService()

    @property
    @abc.abstractmethod
    def system_instruction(self) -> str:
        """System prompt defining the agent's persona and constraints."""
        pass

    @abc.abstractmethod
    def build_prompt(self, context: Dict[str, Any]) -> str:
        """Construct the LLM prompt using orchestrator context."""
        pass

    @abc.abstractmethod
    def get_fallback(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Provide robust fallback output if LLM is unavailable or fails schema validation."""
        pass

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute agent reasoning:
        1. Checks if Gemini is configured.
        2. Calls LLM with structured JSON output expectation.
        3. If unavailable or schema invalid, gracefully returns agent fallback.
        """
        if not self.gemini_service.is_configured():
            logger.info(f"[{self.name}] Gemini not configured, using fallback.")
            return self.get_fallback(context)

        prompt = self.build_prompt(context)
        success, data, error = self.gemini_service.generate_json_response(
            prompt=prompt,
            system_instruction=self.system_instruction,
            temperature=0.25
        )

        if success and isinstance(data, dict):
            return data

        logger.warning(f"[{self.name}] LLM generation unsuccessful ({error}). Falling back.")
        return self.get_fallback(context)
