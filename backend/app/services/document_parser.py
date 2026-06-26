from __future__ import annotations

from io import BytesIO
from pathlib import Path

from docx import Document
from pypdf import PdfReader


SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024


class DocumentParseError(ValueError):
    """Raised when an uploaded document cannot be parsed safely."""


def validate_upload(filename: str, content: bytes) -> str:
    extension = Path(filename).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        raise DocumentParseError(
            f"Unsupported file type '{extension or 'unknown'}'. "
            f"Supported types: {supported}."
        )

    if not content:
        raise DocumentParseError("The uploaded file is empty.")

    if len(content) > MAX_FILE_SIZE_BYTES:
        raise DocumentParseError("The uploaded file exceeds the 5 MB limit.")

    return extension


def extract_text(filename: str, content: bytes) -> str:
    extension = validate_upload(filename, content)

    try:
        if extension == ".txt":
            text = content.decode("utf-8")
        elif extension == ".docx":
            text = _extract_docx_text(content)
        else:
            text = _extract_pdf_text(content)
    except (UnicodeDecodeError, OSError, KeyError, ValueError) as exc:
        raise DocumentParseError(
            "The uploaded document could not be read."
        ) from exc

    cleaned_text = "\n".join(
        line.strip() for line in text.splitlines() if line.strip()
    ).strip()

    if not cleaned_text:
        raise DocumentParseError(
            "No readable text was found in the uploaded document."
        )

    return cleaned_text


def _extract_docx_text(content: bytes) -> str:
    document = Document(BytesIO(content))
    return "\n".join(
        paragraph.text for paragraph in document.paragraphs
        if paragraph.text.strip()
    )


def _extract_pdf_text(content: bytes) -> str:
    reader = PdfReader(BytesIO(content))
    return "\n".join(page.extract_text() or "" for page in reader.pages)
