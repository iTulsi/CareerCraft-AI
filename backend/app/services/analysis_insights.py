from __future__ import annotations

import re
from collections.abc import Iterable

from app.services.baseline_matcher import skill_terms
from app.services.section_parser import detect_sections


REQUIRED_CUES = {
    "must",
    "required",
    "requirement",
    "need",
    "needs",
    "proficient",
    "proficiency",
    "strong",
}
PREFERRED_CUES = {
    "preferred",
    "nice to have",
    "bonus",
    "plus",
}


def build_skill_priorities(
    job_description: str,
    skills: Iterable[str],
) -> list[dict[str, object]]:
    """Rank explicitly detected job skills without inventing requirements."""
    sentences = _sentences(job_description)
    priorities: list[dict[str, object]] = []

    for skill in sorted(set(skills)):
        matching_sentences = [
            sentence for sentence in sentences if _contains_skill(sentence, skill)
        ]
        mentions = sum(_count_skill_mentions(sentence, skill) for sentence in sentences)
        context = " ".join(matching_sentences).casefold()

        if any(cue in context for cue in REQUIRED_CUES):
            priority = "high"
            reason = "The job description presents this skill as required."
        elif any(cue in context for cue in PREFERRED_CUES):
            priority = "low"
            reason = "The job description presents this skill as preferred."
        elif mentions >= 2:
            priority = "high"
            reason = "The skill is mentioned multiple times in the job description."
        else:
            priority = "medium"
            reason = "The skill is explicitly mentioned in the job description."

        priorities.append(
            {
                "skill": skill,
                "mentions": max(mentions, 1),
                "priority": priority,
                "reason": reason,
            }
        )

    priority_order = {"high": 0, "medium": 1, "low": 2}
    return sorted(
        priorities,
        key=lambda item: (
            priority_order[str(item["priority"])],
            -int(item["mentions"]),
            str(item["skill"]),
        ),
    )


def _sentences(text: str) -> list[str]:
    return [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+|\n+", text)
        if sentence.strip()
    ]


def _contains_skill(text: str, skill: str) -> bool:
    return _count_skill_mentions(text, skill) > 0


def _count_skill_mentions(text: str, skill: str) -> int:
    normalized = text.casefold()
    return sum(
        len(
            re.findall(
                rf"(?<![a-z0-9]){re.escape(term)}(?![a-z0-9])",
                normalized,
            )
        )
        for term in skill_terms(skill)
    )


SECTION_LABELS = {
    "general": "General",
    "summary": "Summary",
    "skills": "Skills",
    "experience": "Experience",
    "projects": "Projects",
    "education": "Education",
    "certifications": "Certifications",
    "achievements": "Achievements",
}


def build_skill_evidence(
    resume_text: str,
    matched_skills: Iterable[str],
) -> list[dict[str, object]]:
    """Return concise, inspectable resume evidence for every matched skill."""
    sections = detect_sections(resume_text)
    evidence: list[dict[str, object]] = []

    for skill in sorted(set(matched_skills)):
        matching_sections: list[str] = []
        snippet: str | None = None

        for section, section_text in sections.items():
            if not _contains_skill(section_text, skill):
                continue

            matching_sections.append(SECTION_LABELS.get(section, section.title()))
            if snippet is None:
                snippet = _first_skill_snippet(section_text, skill)

        evidence.append(
            {
                "skill": skill,
                "sections": matching_sections,
                "snippet": snippet,
                "quantified": bool(
                    snippet and re.search(r"\b\d+(?:\.\d+)?(?:%|x|\+)?\b", snippet)
                ),
            }
        )

    return evidence


def _first_skill_snippet(text: str, skill: str) -> str | None:
    fragments = [
        fragment.strip(" \t-*•")
        for fragment in re.split(r"\n+|(?<=[.!?])\s+", text)
        if fragment.strip()
    ]

    for fragment in fragments:
        if _contains_skill(fragment, skill):
            return fragment[:180]

    return None
