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
        "experience and certification",
        "experience and certifications",
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


def _canonical_section(line: str) -> str | None:
    normalized = _normalize_heading(line)

    for canonical, aliases in SECTION_ALIASES.items():
        if normalized in aliases:
            return canonical

    return None


def _restore_flattened_headings(text: str) -> str:
    aliases = sorted(
        {
            alias
            for aliases in SECTION_ALIASES.values()
            for alias in aliases
        },
        key=len,
        reverse=True,
    )

    pattern = re.compile(
        r"(?<![A-Za-z])(" +
        "|".join(re.escape(alias) for alias in aliases) +
        r")(?![A-Za-z])",
        flags=re.IGNORECASE,
    )

    def add_line_breaks(match: re.Match[str]) -> str:
        value = match.group(0)
        letters = re.sub(r"[^A-Za-z]", "", value)

        if letters and letters.isupper():
            return f"\n{value}\n"

        return value

    return pattern.sub(add_line_breaks, text)


def detect_sections(text: str) -> dict[str, str]:
    prepared_text = _restore_flattened_headings(text)

    sections: dict[str, list[str]] = {"general": []}
    current_section = "general"

    for raw_line in prepared_text.splitlines():
        line = raw_line.strip(" \t:-")
        if not line:
            continue

        detected_section = _canonical_section(line)

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
