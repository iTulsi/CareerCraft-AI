from app.services.interview_questions import build_interview_questions


def test_builds_questions_from_skills_and_resume_sections() -> None:
    questions = build_interview_questions(
        matched_skills=["python", "fastapi", "docker", "react"],
        missing_skills=["aws", "sql", "mongodb"],
        found_sections=["Projects", "Experience"],
    )

    categories = [question["category"] for question in questions]

    assert categories.count("technical") == 3
    assert categories.count("learning_gap") == 2
    assert categories.count("behavioral") == 2
    assert "Python" in questions[0]["question"]
    assert all(question["answer_outline"] for question in questions)


def test_returns_general_question_when_no_evidence_is_available() -> None:
    questions = build_interview_questions(
        matched_skills=[],
        missing_skills=[],
        found_sections=[],
    )

    assert questions == [
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
    ]
