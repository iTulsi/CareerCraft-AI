import re
from collections.abc import Iterable


DEFAULT_SKILLS = {
    "python",
    "java",
    "javascript",
    "typescript",
    "react",
    "fastapi",
    "flask",
    "sql",
    "mongodb",
    "docker",
    "git",
    "github actions",
    "machine learning",
    "deep learning",
    "pytorch",
    "tensorflow",
    "scikit-learn",
    "pandas",
    "numpy",
    "langchain",
    "langgraph",
    "rag",
    "embeddings",
    "vector database",
    "faiss",
    "chromadb",
    "llm",
    "nlp",
    "rest api",
    "aws",
    "azure",
    "gcp",
}


SKILL_ALIASES: dict[str, set[str]] = {
    "github actions": {"github actions", "gh actions"},
    "machine learning": {"machine learning", "ml"},
    "rest api": {"rest api", "rest apis", "restful api", "restful apis"},
    "scikit-learn": {"scikit-learn", "scikit learn", "sklearn"},
}


def skill_terms(skill: str) -> tuple[str, ...]:
    """Return accepted spellings for one canonical skill name."""
    terms = SKILL_ALIASES.get(skill, {skill})
    return tuple(sorted(terms, key=len, reverse=True))


def _normalize(text: str) -> str:
    lowered = text.lower()
    return re.sub(r"\s+", " ", lowered).strip()


def extract_skills(text: str, vocabulary: Iterable[str] = DEFAULT_SKILLS) -> set[str]:
    normalized = _normalize(text)
    return {
        skill
        for skill in vocabulary
        if any(
            re.search(
                rf"(?<![a-z0-9]){re.escape(term)}(?![a-z0-9])",
                normalized,
            )
            for term in skill_terms(skill)
        )
    }


def calculate_skill_match(resume_text: str, job_description: str) -> dict[str, object]:
    resume_skills = extract_skills(resume_text)
    required_skills = extract_skills(job_description)

    if not required_skills:
        return {
            "matched_skills": [],
            "missing_skills": [],
            "match_score": 0.0,
        }

    matched = sorted(resume_skills & required_skills)
    missing = sorted(required_skills - resume_skills)
    score = round((len(matched) / len(required_skills)) * 100, 2)

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "match_score": score,
    }
