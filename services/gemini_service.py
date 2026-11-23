"""Google Gemini API service wrapper using official google-genai SDK."""
import json
import logging
import os
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
        self._explicit_key: bool = (api_key is not None)
        if api_key is not None:
            raw_key = api_key
        else:
            raw_key = Config.GEMINI_API_KEY

        self.api_key = (raw_key or "").strip().strip('"').strip("'")
        self.model = model or Config.GEMINI_MODEL or "gemma-4-31b-it"
        self._client: Optional[genai.Client] = None
        self._init_client()

    def _is_gemma_model(self) -> bool:
        """Check if the current model is a Gemma model (which does not support structured JSON output mode)."""
        return "gemma" in self.model.lower()

    def _init_client(self):
        """Initialize Google GenAI client if API key is present."""
        if self.api_key:
            try:
                self._client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logger.error(f"Failed to initialize Gemini Client: {str(e)}")
                self._client = None
        else:
            self._client = None

    def is_configured(self) -> bool:
        """Check if a valid API key is configured. Dynamically re-checks environment if not explicitly set."""
        # If in a pytest test environment or an explicit empty key was provided, do not auto-reload
        if not self._explicit_key and not os.getenv("PYTEST_CURRENT_TEST"):
            if not self.api_key:
                from config import load_app_env
                load_app_env(override=False)
                current_key = (os.getenv("GEMINI_API_KEY") or "").strip().strip('"').strip("'")
                if current_key:
                    self.api_key = current_key
                    self._init_client()
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
        Send prompt to model and parse structured JSON.
        Gemini models use response_mime_type for guaranteed JSON.
        Gemma models rely on prompt instructions + robust JSON extraction.
        Returns (success, parsed_data, error_message).
        """
        if not self.is_configured():
            return False, None, "API key is not configured."

        try:
            # Gemma models do not support response_mime_type or system_instruction
            # as config parameters; we embed them into the prompt instead.
            if self._is_gemma_model():
                full_prompt = ""
                if system_instruction:
                    full_prompt += f"{system_instruction}\n\n"
                full_prompt += prompt
                full_prompt += "\n\nIMPORTANT: You MUST respond ONLY with a single valid JSON object. No markdown, no code fences, no explanation — just raw JSON."

                config = types.GenerateContentConfig(
                    temperature=temperature
                )

                response = self._client.models.generate_content(
                    model=self.model,
                    contents=full_prompt,
                    config=config
                )
            else:
                # Gemini models support structured JSON output mode
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
                return False, None, "Empty response received from model."

            parsed = self.extract_clean_json(response.text)
            if parsed is None:
                logger.warning(f"Failed to parse JSON from model response: {response.text[:200]}...")
                return False, None, "Model output was not valid JSON."

            return True, parsed, None

        except APIError as ae:
            error_msg = str(ae)
            if self.api_key and self.api_key in error_msg:
                error_msg = error_msg.replace(self.api_key, "[REDACTED_API_KEY]")
            logger.error(f"API Error: {error_msg}")
            return False, None, f"API Error: {error_msg}"

        except Exception as e:
            err_str = str(e)
            if self.api_key and self.api_key in err_str:
                err_str = err_str.replace(self.api_key, "[REDACTED_API_KEY]")
            logger.error(f"Unexpected error calling API: {err_str}")
            return False, None, f"AI generation failed: {err_str}"

    def extract_text_from_file(
        self,
        file_bytes: bytes,
        mime_type: str = "application/pdf"
    ) -> Tuple[bool, Optional[str], str]:
        """
        Use Gemini's multimodal capabilities (OCR) to extract text from a PDF or image file.
        Returns (success, error_message, extracted_text).
        """
        if not self.is_configured():
            return False, "Gemini API key is not configured.", ""

        try:
            part = types.Part.from_bytes(data=file_bytes, mime_type=mime_type)
            prompt = (
                "You are an expert document parser and OCR engine. "
                "Extract all text, sections, work experience, projects, skills, education, contact info, "
                "and details from this resume document verbatim. "
                "Preserve all names, dates, numbers, and bullet points. "
                "Output ONLY the extracted raw plain text without code fences or conversational markdown."
            )

            response = self._client.models.generate_content(
                model=self.model,
                contents=[part, prompt]
            )

            if not response or not response.text:
                return False, "Gemini returned empty text for document OCR.", ""

            return True, None, response.text.strip()

        except Exception as e:
            err_msg = str(e)
            if self.api_key and self.api_key in err_msg:
                err_msg = err_msg.replace(self.api_key, "[REDACTED_API_KEY]")
            logger.error(f"Gemini multimodal OCR failed: {err_msg}")
            return False, f"AI OCR extraction failed: {err_msg}", ""
