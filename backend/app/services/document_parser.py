from __future__ import annotations

import re
import unicodedata
from io import BytesIO
from pathlib import Path

import pdfplumber
from docx import Document
from pypdf import PdfReader


SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024

LIGATURE_REPLACEMENTS = {
    "\ufb00": "ff",
    "\ufb01": "fi",
    "\ufb02": "fl",
    "\ufb03": "ffi",
    "\ufb04": "ffl",
    "\ufb05": "ft",
    "\ufb06": "st",
    "\u00a0": " ",
    "\u00ad": "",
}


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


def normalize_extracted_text(text: str) -> str:
    for source, replacement in LIGATURE_REPLACEMENTS.items():
        text = text.replace(source, replacement)

    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    cleaned_lines: list[str] = []
    for raw_line in text.splitlines():
        line = re.sub(r"[ \t]+", " ", raw_line).strip()
        if line:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()


def extract_text(filename: str, content: bytes) -> str:
    extension = validate_upload(filename, content)

    try:
        if extension == ".txt":
            raw_text = content.decode("utf-8")
        elif extension == ".docx":
            raw_text = _extract_docx_text(content)
        else:
            raw_text = _extract_pdf_text(content)
    except (UnicodeDecodeError, OSError, KeyError, ValueError) as exc:
        raise DocumentParseError(
            "The uploaded document could not be read."
        ) from exc

    cleaned_text = normalize_extracted_text(raw_text)

    if not cleaned_text:
        raise DocumentParseError(
            "No readable text was found in the uploaded document."
        )

    return cleaned_text


def _extract_docx_text(content: bytes) -> str:
    document = Document(BytesIO(content))
    return "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    )


def _extract_pdf_text(content: bytes) -> str:
    plumber_text = _extract_pdf_with_pdfplumber(content)
    if plumber_text.strip():
        return plumber_text

    return _extract_pdf_with_pypdf(content)


def _extract_pdf_with_pdfplumber(content: bytes) -> str:
    pages: list[str] = []

    with pdfplumber.open(BytesIO(content)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text(
                x_tolerance=2,
                y_tolerance=3,
                layout=True,
            )
            if page_text:
                pages.append(page_text)

    return "\n".join(pages)


def _extract_pdf_with_pypdf(content: bytes) -> str:
    reader = PdfReader(BytesIO(content))
    pages: list[str] = []

    for page in reader.pages:
        try:
            page_text = page.extract_text(extraction_mode="layout") or ""
        except TypeError:
            page_text = page.extract_text() or ""

        if page_text:
            pages.append(page_text)

    return "\n".join(pages)
