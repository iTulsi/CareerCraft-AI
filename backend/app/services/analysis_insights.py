from __future__ import annotations

import re
from collections.abc import Iterable

from app.services.baseline_matcher import skill_terms


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
