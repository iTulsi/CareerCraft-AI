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


ACTION_VERBS = {
    "achieved",
    "automated",
    "built",
    "created",
    "delivered",
    "designed",
    "developed",
    "implemented",
    "improved",
    "increased",
    "launched",
    "led",
    "optimized",
    "reduced",
    "shipped",
}
BULLET_PATTERN = re.compile(r"^\s*(?:[-*•]|\d+[.)])\s+")
NUMBER_PATTERN = re.compile(r"\b\d+(?:\.\d+)?(?:%|x|\+|k|m)?\b", re.IGNORECASE)


def analyze_resume_quality(resume_text: str) -> dict[str, object]:
    """Measure observable writing signals without assigning a hiring score."""
    non_empty_lines = [line.strip() for line in resume_text.splitlines() if line.strip()]
    bullet_lines = [line for line in non_empty_lines if BULLET_PATTERN.match(line)]
    evidence_lines = bullet_lines or non_empty_lines

    action_oriented = sum(_starts_with_action_verb(line) for line in evidence_lines)
    quantified = sum(bool(NUMBER_PATTERN.search(line)) for line in evidence_lines)
    bullet_count = len(bullet_lines)

    suggestions: list[str] = []
    if bullet_count == 0:
        suggestions.append(
            "Use concise bullet points for project and experience achievements."
        )
    if evidence_lines and action_oriented / len(evidence_lines) < 0.5:
        suggestions.append(
            "Start more achievement statements with specific action verbs."
        )
    if evidence_lines and quantified / len(evidence_lines) < 0.3:
        suggestions.append(
            "Quantify impact where truthful with counts, percentages, time, or scale."
        )
    if len(resume_text.split()) < 150:
        suggestions.append(
            "The extracted resume is brief; verify that parsing captured all sections."
        )

    return {
        "word_count": len(resume_text.split()),
        "bullet_count": bullet_count,
        "action_oriented_statements": action_oriented,
        "quantified_statements": quantified,
        "quantified_statement_ratio": round(
            (quantified / len(evidence_lines)) * 100 if evidence_lines else 0.0,
            2,
        ),
        "suggestions": suggestions,
    }


def _starts_with_action_verb(line: str) -> bool:
    cleaned = BULLET_PATTERN.sub("", line).strip()
    first_word = re.split(r"\W+", cleaned.casefold(), maxsplit=1)[0]
    return first_word in ACTION_VERBS


EXPERIENCE_PATTERN = re.compile(
    r"\b\d+(?:\s*[-–]\s*\d+)?\+?\s*(?:years?|yrs?)\b",
    re.IGNORECASE,
)
SENIORITY_TERMS = {
    "intern": "Intern",
    "internship": "Intern",
    "junior": "Junior",
    "entry level": "Entry level",
    "mid level": "Mid level",
    "senior": "Senior",
    "lead": "Lead",
    "staff": "Staff",
    "principal": "Principal",
}
EDUCATION_TERMS = {
    "bachelor": "Bachelor's degree",
    "b.tech": "B.Tech",
    "btech": "B.Tech",
    "master": "Master's degree",
    "m.tech": "M.Tech",
    "mtech": "M.Tech",
    "phd": "PhD",
    "computer science": "Computer Science",
}
WORK_ARRANGEMENTS = {
    "remote": "Remote",
    "hybrid": "Hybrid",
    "on-site": "On-site",
    "onsite": "On-site",
    "work from home": "Remote",
}


def analyze_job_requirements(job_description: str) -> dict[str, list[str]]:
    """Extract only explicit role requirements and logistical signals."""
    normalized = job_description.casefold()
    experience_requirements = sorted(
        {match.group(0) for match in EXPERIENCE_PATTERN.finditer(job_description)},
        key=str.casefold,
    )
    seniority = _labels_found(normalized, SENIORITY_TERMS)
    education = _labels_found(normalized, EDUCATION_TERMS)
    work_arrangements = _labels_found(normalized, WORK_ARRANGEMENTS)

    return {
        "experience_requirements": experience_requirements,
        "seniority_signals": seniority,
        "education_requirements": education,
        "work_arrangements": work_arrangements,
    }


def _labels_found(text: str, vocabulary: dict[str, str]) -> list[str]:
    return sorted(
        {
            label
            for term, label in vocabulary.items()
            if re.search(
                rf"(?<![a-z0-9]){re.escape(term)}(?![a-z0-9])",
                text,
            )
        }
    )
