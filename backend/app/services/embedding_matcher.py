from __future__ import annotations

import math
from collections.abc import Callable, Sequence
from functools import lru_cache
from typing import Any


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

Encoder = Callable[[list[str]], Sequence[Sequence[float]]]


class SemanticModelUnavailable(RuntimeError):
    """Raised when the optional semantic model cannot be loaded."""


@lru_cache(maxsize=1)
def _load_model() -> Any:
    try:
        from sentence_transformers import SentenceTransformer

        return SentenceTransformer(MODEL_NAME)
    except Exception as exc:
        raise SemanticModelUnavailable(
            "The optional semantic model is not available."
        ) from exc


def calculate_semantic_similarity(
    resume_text: str,
    job_description: str,
    *,
    encoder: Encoder | None = None,
) -> float:
    texts = [resume_text.strip(), job_description.strip()]

    if encoder is None:
        model = _load_model()
        vectors = model.encode(texts)
    else:
        vectors = encoder(texts)

    if len(vectors) != 2:
        raise ValueError("The encoder must return exactly two vectors.")

    similarity = _cosine_similarity(vectors[0], vectors[1])
    return round(max(0.0, min(1.0, similarity)) * 100, 2)


def _cosine_similarity(
    left: Sequence[float],
    right: Sequence[float],
) -> float:
    if len(left) != len(right) or len(left) == 0:
        raise ValueError("Embedding vectors must have the same non-zero length.")

    dot_product = sum(
        float(left_value) * float(right_value)
        for left_value, right_value in zip(left, right, strict=True)
    )
    left_norm = math.sqrt(sum(float(value) ** 2 for value in left))
    right_norm = math.sqrt(sum(float(value) ** 2 for value in right))

    if left_norm == 0 or right_norm == 0:
        raise ValueError("Embedding vectors must not be zero vectors.")

    return dot_product / (left_norm * right_norm)
