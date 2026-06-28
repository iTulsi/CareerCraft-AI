from __future__ import annotations


MAX_TECHNICAL_QUESTIONS = 3
MAX_GAP_QUESTIONS = 2

DISPLAY_NAMES = {
    "ai": "AI",
    "api": "API",
    "aws": "AWS",
    "css": "CSS",
    "docker": "Docker",
    "fastapi": "FastAPI",
    "git": "Git",
    "github actions": "GitHub Actions",
    "html": "HTML",
    "javascript": "JavaScript",
    "ml": "ML",
    "mongodb": "MongoDB",
    "mysql": "MySQL",
    "node.js": "Node.js",
    "numpy": "NumPy",
    "pandas": "Pandas",
    "postgresql": "PostgreSQL",
    "python": "Python",
    "pytorch": "PyTorch",
    "react": "React",
    "sql": "SQL",
    "typescript": "TypeScript",
}


def build_interview_questions(
    *,
    matched_skills: list[str],
    missing_skills: list[str],
    found_sections: list[str],
) -> list[dict[str, str]]:
    questions: list[dict[str, str]] = []

    for skill in matched_skills[:MAX_TECHNICAL_QUESTIONS]:
        label = _display_name(skill)
        questions.append(
            {
                "category": "technical",
                "question": (
                    f"Explain how you used {label} in a real project. "
                    "What design decision or trade-off did you make?"
                ),
                "answer_outline": (
                    "Describe the problem, your specific implementation, "
                    "one trade-off you considered, and a measurable result."
                ),
            }
        )

    for skill in missing_skills[:MAX_GAP_QUESTIONS]:
        label = _display_name(skill)
        questions.append(
            {
                "category": "learning_gap",
                "question": (
                    f"This role asks for {label}. What relevant experience "
                    "do you have, and how would you close this gap?"
                ),
                "answer_outline": (
                    "Be honest about your current level, connect adjacent "
                    "experience, and give a concrete learning or project plan."
                ),
            }
        )

    section_names = set(found_sections)

    if "Projects" in section_names:
        questions.append(
            {
                "category": "behavioral",
                "question": (
                    "Tell me about a project where the requirements changed "
                    "after you had already started building."
                ),
                "answer_outline": (
                    "Use STAR: explain the situation, your responsibility, "
                    "how you adapted, and the final result."
                ),
            }
        )

    if "Experience" in section_names:
        questions.append(
            {
                "category": "behavioral",
                "question": (
                    "Describe a time you found and fixed a reliability, "
                    "performance, or quality problem."
                ),
                "answer_outline": (
                    "Explain how you detected the problem, investigated it, "
                    "implemented the fix, and verified the improvement."
                ),
            }
        )

    if not questions:
        questions.append(
            {
                "category": "behavioral",
                "question": (
                    "Tell me about a difficult technical problem you solved "
                    "and what you learned from it."
                ),
                "answer_outline": (
                    "Use a specific example and explain the problem, your "
                    "actions, the outcome, and what you would improve next time."
                ),
            }
        )

    return questions


def _display_name(skill: str) -> str:
    return DISPLAY_NAMES.get(skill.casefold(), skill)
