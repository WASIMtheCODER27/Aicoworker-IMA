"""Google Gemini API service wrapper using official google-genai SDK."""
import json
import logging
import re
from typing import Dict, Any, Optional, Tuple
from google import genai
from google.genai import types
from google.genai.errors import APIError
from config import Config

logger = logging.getLogger(__name__)

class GeminiService:
    """Manages communication with Google Gemini API."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = (api_key or Config.GEMINI_API_KEY).strip()
        self.model = model or Config.GEMINI_MODEL or "gemini-2.5-flash"
        self._client: Optional[genai.Client] = None

        if self.api_key:
            try:
                self._client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logger.error(f"Failed to initialize Gemini Client: {str(e)}")
                self._client = None

    def is_configured(self) -> bool:
        """Check if a valid API key is configured."""
        return bool(self.api_key and self._client is not None)

    @staticmethod
    def extract_clean_json(text: str) -> Optional[Dict[str, Any]]:
        """
        Extract and parse JSON from raw text or markdown code fences.
        """
        if not text or not isinstance(text, str):
            return None

        clean_text = text.strip()

        # Try direct parse
        try:
            return json.loads(clean_text)
        except json.JSONDecodeError:
            pass

        # Match ```json ... ``` or ``` ... ```
        fence_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', clean_text, re.IGNORECASE)
        if fence_match:
            try:
                return json.loads(fence_match.group(1).strip())
            except json.JSONDecodeError:
                pass

        # Find first { and last }
        start = clean_text.find('{')
        end = clean_text.rfind('}')
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(clean_text[start:end + 1])
            except json.JSONDecodeError:
                pass

        return None

    def generate_json_response(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.2
    ) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
        """
        Send prompt to Gemini model and parse structured JSON.
        Returns (success, parsed_data, error_message).
        """
        if not self.is_configured():
            return False, None, "Gemini API key is not configured."

        try:
            config = types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=temperature,
                system_instruction=system_instruction
            )

            response = self._client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=config
            )

            if not response or not response.text:
                return False, None, "Empty response received from Gemini model."

            parsed = self.extract_clean_json(response.text)
            if parsed is None:
                logger.warning(f"Failed to parse JSON from Gemini response: {response.text[:200]}...")
                return False, None, "Model output was not valid JSON."

            return True, parsed, None

        except APIError as ae:
            error_msg = str(ae)
            # Mask any accidental key leakage in error strings
            if self.api_key and self.api_key in error_msg:
                error_msg = error_msg.replace(self.api_key, "[REDACTED_API_KEY]")
            logger.error(f"Gemini API Error: {error_msg}")
            return False, None, f"Gemini API Error: {error_msg}"

        except Exception as e:
            err_str = str(e)
            if self.api_key and self.api_key in err_str:
                err_str = err_str.replace(self.api_key, "[REDACTED_API_KEY]")
            logger.error(f"Unexpected error calling Gemini API: {err_str}")
            return False, None, f"AI generation failed: {err_str}"
