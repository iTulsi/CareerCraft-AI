from __future__ import annotations

from app.services.analysis_insights import (
    analyze_resume_quality,
    build_skill_priorities,
)
from app.services.baseline_matcher import calculate_skill_match
from app.services.section_parser import detect_sections


REQUIRED_SECTIONS = {
    "skills": "Skills",
    "experience": "Experience",
    "projects": "Projects",
    "education": "Education",
}

SKILL_WEIGHT = 0.75
STRUCTURE_WEIGHT = 0.25


def calculate_resume_assessment(
    resume_text: str,
    job_description: str,
) -> tuple[dict[str, object], dict[str, object]]:
    skill_match = calculate_skill_match(
        resume_text=resume_text,
        job_description=job_description,
    )
    sections = detect_sections(resume_text)

    found_sections = [
        label
        for key, label in REQUIRED_SECTIONS.items()
        if sections.get(key)
    ]
    missing_sections = [
        label
        for key, label in REQUIRED_SECTIONS.items()
        if not sections.get(key)
    ]

    skill_score = float(skill_match["match_score"])
    structure_score = round(
        (len(found_sections) / len(REQUIRED_SECTIONS)) * 100,
        2,
    )
    overall_score = round(
        (skill_score * SKILL_WEIGHT)
        + (structure_score * STRUCTURE_WEIGHT),
        2,
    )

    assessment: dict[str, object] = {
        "overall_score": overall_score,
        "skill_score": skill_score,
        "structure_score": structure_score,
        "found_sections": found_sections,
        "missing_sections": missing_sections,
        "recommendations": _build_recommendations(
            missing_skills=list(skill_match["missing_skills"]),
            missing_sections=missing_sections,
            skill_priorities=build_skill_priorities(
                job_description,
                list(skill_match["missing_skills"]),
            ),
            quality_suggestions=list(
                analyze_resume_quality(resume_text)["suggestions"]
            ),
        ),
    }

    return skill_match, assessment


def _build_recommendations(
    missing_skills: list[str],
    missing_sections: list[str],
    skill_priorities: list[dict[str, object]],
    quality_suggestions: list[str],
) -> list[str]:
    recommendations: list[str] = []

    high_priority_missing = [
        str(item["skill"])
        for item in skill_priorities
        if item["priority"] == "high"
    ]
    if high_priority_missing:
        recommendations.append(
            "Prioritize truthful evidence or focused learning for the highest-demand "
            f"gaps: {', '.join(high_priority_missing)}."
        )

    if missing_skills:
        skill_list = ", ".join(missing_skills)
        recommendations.append(
            "Add evidence for these skills only where truthful: "
            f"{skill_list}. Otherwise, treat them as learning priorities."
        )

    for section in missing_sections:
        recommendations.append(
            f"Add a dedicated {section} section with relevant, verifiable evidence."
        )

    recommendations.extend(
        suggestion
        for suggestion in quality_suggestions
        if suggestion not in recommendations
    )

    if not recommendations:
        recommendations.append(
            "Tailor the strongest bullets to this role and quantify impact "
            "where supporting evidence exists."
        )

    return recommendations
