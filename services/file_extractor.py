"""Secure text extraction from PDF, TXT, and Markdown resumes."""
import logging
import os
import re
import tempfile
from pathlib import Path
from typing import Tuple, Optional, Any
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import pypdf
from pypdf.errors import PdfReadError

logger = logging.getLogger(__name__)

MAX_TEXT_CHARACTERS = 25000

def sanitize_extracted_text(text: str) -> str:
    """Clean extracted text from control chars, excessive whitespace, and potential prompt markers."""
    if not text:
        return ""
    # Strip null and control characters
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', ' ', text)
    # Normalize multiple newlines and spaces
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]{2,}', ' ', text)
    return text.strip()

def extract_from_pdf(filepath: Path, gemini_service: Optional[Any] = None) -> Tuple[bool, Optional[str], str]:
    """
    Extract readable text from a PDF file using pypdf.
    If the PDF is image-based or lacks a standard text layer, falls back to Gemini Multimodal OCR.
    """
    try:
        reader = pypdf.PdfReader(str(filepath))
        if reader.is_encrypted:
            try:
                # Attempt empty password decrypt
                reader.decrypt("")
            except Exception:
                return False, "The PDF file is password protected and cannot be read.", ""

        pages_text = []
        total_pages = len(reader.pages)
        if total_pages == 0:
            return False, "The PDF contains no readable pages.", ""

        for idx, page in enumerate(reader.pages):
            try:
                # 1. Standard text extraction
                page_content = page.extract_text() or ""

                # 2. Layout extraction mode if standard extraction is empty
                if not page_content.strip():
                    try:
                        page_content = page.extract_text(extraction_mode="layout") or ""
                    except Exception:
                        pass

                # 3. Orientations check if still empty
                if not page_content.strip():
                    try:
                        page_content = page.extract_text(orientations=(0, 90, 180, 270)) or ""
                    except Exception:
                        pass

                if page_content.strip():
                    pages_text.append(page_content.strip())
            except Exception:
                # Continue reading remaining pages if one fails
                continue

        full_text = "\n\n".join(pages_text)
        cleaned = sanitize_extracted_text(full_text)

        # If local extraction produced substantial text, return it
        if cleaned and len(cleaned) >= 40:
            return True, None, cleaned[:MAX_TEXT_CHARACTERS]

        # If local text is empty or very short (< 40 chars), try Gemini Multimodal AI OCR
        if gemini_service and hasattr(gemini_service, "is_configured") and gemini_service.is_configured():
            try:
                logger.info("Local PDF extraction produced empty or sparse text. Triggering Gemini Multimodal OCR.")
                raw_bytes = filepath.read_bytes()
                ocr_success, ocr_err, ocr_text = gemini_service.extract_text_from_file(raw_bytes, mime_type="application/pdf")
                if ocr_success and ocr_text.strip():
                    cleaned_ocr = sanitize_extracted_text(ocr_text)
                    if cleaned_ocr:
                        logger.info("Successfully extracted resume text via Gemini Multimodal OCR.")
                        return True, None, cleaned_ocr[:MAX_TEXT_CHARACTERS]
                elif ocr_err:
                    logger.warning(f"Gemini OCR extraction failed: {ocr_err}")
            except Exception as ocr_ex:
                logger.warning(f"Error during Gemini OCR fallback: {str(ocr_ex)}")

        if not cleaned:
            return False, "Could not extract text from the PDF. It may contain scanned images without OCR.", ""

        return True, None, cleaned[:MAX_TEXT_CHARACTERS]

    except PdfReadError as pre:
        return False, f"Invalid or corrupted PDF file: {str(pre)}", ""
    except Exception as e:
        return False, f"Failed to parse PDF document: {str(e)}", ""

def extract_from_plaintext(filepath: Path) -> Tuple[bool, Optional[str], str]:
    """Extract text from TXT or Markdown files."""
    try:
        raw_bytes = filepath.read_bytes()
        # Attempt UTF-8 decoding first, then Latin-1 with replacement
        try:
            content = raw_bytes.decode("utf-8")
        except UnicodeDecodeError:
            content = raw_bytes.decode("latin-1", errors="replace")

        cleaned = sanitize_extracted_text(content)
        if not cleaned:
            return False, "Uploaded text document contains no readable text.", ""

        return True, None, cleaned[:MAX_TEXT_CHARACTERS]
    except Exception as e:
        return False, f"Failed to read text file: {str(e)}", ""

def extract_resume_text(
    file: Optional[FileStorage],
    gemini_service: Optional[Any] = None
) -> Tuple[bool, Optional[str], str]:
    """
    Safely process and extract text from an uploaded resume file.
    Guarantees temporary file cleanup.
    Returns (success, error_message, extracted_text).
    """
    if file is None or not file.filename:
        return True, None, ""

    raw_filename = secure_filename(file.filename) or "resume.tmp"
    ext = raw_filename.rsplit(".", 1)[-1].lower() if "." in raw_filename else ""

    # Create a secure temporary file
    temp_dir = tempfile.gettempdir()
    temp_path = Path(temp_dir) / f"careerpilot_{os.getpid()}_{raw_filename}"

    try:
        file.seek(0)
        file.save(str(temp_path))

        if ext == "pdf":
            success, err, text = extract_from_pdf(temp_path, gemini_service=gemini_service)
        elif ext in ("txt", "md"):
            success, err, text = extract_from_plaintext(temp_path)
        else:
            return False, f"Unsupported file extension '.{ext}'. Supported: PDF, TXT, MD.", ""

        return success, err, text

    finally:
        # Guarantee cleanup of temporary file immediately
        try:
            if temp_path.exists():
                temp_path.unlink()
        except Exception:
            pass
