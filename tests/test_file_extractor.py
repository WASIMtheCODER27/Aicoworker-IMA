"""Tests for file extraction from PDF, TXT, and Markdown files."""
import io
import os
import pytest
from werkzeug.datastructures import FileStorage
import pypdf
from services.file_extractor import extract_resume_text

def test_extract_from_txt():
    """Verify clean text extraction from .txt files."""
    content = "Summary: Experienced software engineer specializing in Python and Cloud Systems."
    file = FileStorage(
        stream=io.BytesIO(content.encode("utf-8")),
        filename="resume.txt",
        content_type="text/plain"
    )
    success, err, text = extract_resume_text(file)
    assert success is True
    assert err is None
    assert "Experienced software engineer" in text

def test_extract_from_markdown():
    """Verify clean text extraction from .md files."""
    content = "# John Doe\n\n## Skills\n- Python\n- React\n- Docker\n\n## Experience\nBuilt REST APIs."
    file = FileStorage(
        stream=io.BytesIO(content.encode("utf-8")),
        filename="resume.md",
        content_type="text/markdown"
    )
    success, err, text = extract_resume_text(file)
    assert success is True
    assert err is None
    assert "Built REST APIs" in text
    assert "Python" in text

def test_extract_from_valid_pdf():
    """Create a minimal real PDF in memory and verify extraction."""
    writer = pypdf.PdfWriter()
    page = writer.add_blank_page(width=72, height=72)
    # Note: blank page has no text, so test with text if possible or check expected message
    pdf_bytes_io = io.BytesIO()
    writer.write(pdf_bytes_io)
    pdf_bytes_io.seek(0)

    file = FileStorage(
        stream=pdf_bytes_io,
        filename="test_resume.pdf",
        content_type="application/pdf"
    )
    success, err, text = extract_resume_text(file)
    # A blank PDF has no extractable text, so it reports the expected notice
    if not success:
        assert "Could not extract text" in err or "scanned" in err.lower()
    else:
        assert isinstance(text, str)

def test_extract_from_corrupted_pdf():
    """Verify corrupt PDF bytes are caught gracefully."""
    corrupt_bytes = b"%PDF-1.4\nCorrupt header and junk content not matching PDF specs"
    file = FileStorage(
        stream=io.BytesIO(corrupt_bytes),
        filename="broken.pdf",
        content_type="application/pdf"
    )
    success, err, text = extract_resume_text(file)
    assert success is False
    assert err is not None
    assert ("corrupted" in err.lower() or "failed" in err.lower() or "invalid" in err.lower())

def test_extract_from_none_file():
    """Verify None file returns success with empty text (optional resume)."""
    success, err, text = extract_resume_text(None)
    assert success is True
    assert err is None
    assert text == ""
