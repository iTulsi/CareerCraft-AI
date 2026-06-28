import math

import pytest

from app.services.embedding_matcher import calculate_semantic_similarity


def test_semantic_similarity_uses_cosine_similarity() -> None:
    def fake_encoder(texts: list[str]) -> list[list[float]]:
        assert len(texts) == 2
        return [[1.0, 0.0], [1.0, 1.0]]

    score = calculate_semantic_similarity(
        "Python backend engineer",
        "Backend role using Python",
        encoder=fake_encoder,
    )

    assert score == round((1 / math.sqrt(2)) * 100, 2)


def test_semantic_similarity_rejects_zero_vectors() -> None:
    def fake_encoder(_: list[str]) -> list[list[float]]:
        return [[0.0, 0.0], [1.0, 0.0]]

    with pytest.raises(ValueError, match="zero vectors"):
        calculate_semantic_similarity(
            "Resume text",
            "Job description",
            encoder=fake_encoder,
        )



def test_similarity_accepts_array_like_vectors() -> None:
    from app.services.embedding_matcher import calculate_semantic_similarity

    class ArrayLikeVector(list):
        def __bool__(self) -> bool:
            raise ValueError("The truth value is ambiguous.")

    def encoder(texts: list[str]) -> list[ArrayLikeVector]:
        assert len(texts) == 2
        return [
            ArrayLikeVector([1.0, 0.0]),
            ArrayLikeVector([1.0, 0.0]),
        ]

    score = calculate_semantic_similarity(
        "Python FastAPI developer",
        "Python API engineer",
        encoder=encoder,
    )

    assert score == 100.0
