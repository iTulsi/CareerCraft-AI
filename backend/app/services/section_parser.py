from __future__ import annotations

import re


SECTION_ALIASES = {
    "summary": {
        "summary",
        "professional summary",
        "profile",
        "objective",
        "career objective",
    },
    "skills": {
        "skills",
        "technical skills",
        "core competencies",
        "technologies",
    },
    "experience": {
        "experience",
        "work experience",
        "professional experience",
        "employment",
    },
    "projects": {
        "projects",
        "personal projects",
        "academic projects",
        "key projects",
    },
    "education": {
        "education",
        "academic background",
        "qualifications",
    },
    "certifications": {
        "certifications",
        "certificates",
        "licenses and certifications",
    },
    "achievements": {
        "achievements",
        "awards",
        "honors",
    },
}


def _normalize_heading(line: str) -> str:
    normalized = re.sub(r"[^a-zA-Z ]", " ", line).lower()
    return re.sub(r"\s+", " ", normalized).strip()


def detect_sections(text: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {"general": []}
    current_section = "general"

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        normalized = _normalize_heading(line)
        detected_section = next(
            (
                canonical
                for canonical, aliases in SECTION_ALIASES.items()
                if normalized in aliases
            ),
            None,
        )

        if detected_section is not None:
            current_section = detected_section
            sections.setdefault(current_section, [])
            continue

        sections.setdefault(current_section, []).append(line)

    return {
        section: "\n".join(lines).strip()
        for section, lines in sections.items()
        if lines
    }
