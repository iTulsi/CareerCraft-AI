from __future__ import annotations


SEMANTIC_STATUSES = {
    "available",
    "unavailable",
    "not_requested",
}


def build_evaluation_comparison(
    *,
    deterministic_score: float,
    semantic_score: float | None,
    semantic_status: str,
) -> dict[str, object]:
    """Compare existing matcher outputs without combining their scores."""
    _validate_score(deterministic_score, name="deterministic_score")

    if semantic_status not in SEMANTIC_STATUSES:
        raise ValueError("semantic_status is not supported.")

    if semantic_status != "available":
        interpretation = (
            "Request semantic comparison to compare explicit skill coverage "
            "with document-level meaning."
            if semantic_status == "not_requested"
            else (
                "The semantic model was unavailable, so only deterministic "
                "skill coverage can currently be evaluated."
            )
        )

        return {
            "status": semantic_status,
            "deterministic_score": deterministic_score,
            "semantic_score": None,
            "score_gap": None,
            "gap_category": "not_available",
            "interpretation": interpretation,
        }

    if semantic_score is None:
        raise ValueError(
            "semantic_score is required when semantic_status is available."
        )

    _validate_score(semantic_score, name="semantic_score")
    score_gap = round(abs(deterministic_score - semantic_score), 2)

    if score_gap <= 10:
        gap_category = "close"
        interpretation = (
            "The scores are close, but they measure different signals: "
            "explicit skill coverage and document-level semantic similarity."
        )
    elif score_gap <= 25:
        gap_category = "moderate"
        interpretation = (
            "The methods show a moderate difference. Review the matched skills "
            "and resume wording instead of treating either score as definitive."
        )
    else:
        gap_category = "wide"
        interpretation = (
            "The methods differ substantially. The resume may express relevant "
            "meaning without enough explicit skills, or contain keywords without "
            "strong overall alignment."
        )

    return {
        "status": "available",
        "deterministic_score": deterministic_score,
        "semantic_score": semantic_score,
        "score_gap": score_gap,
        "gap_category": gap_category,
        "interpretation": interpretation,
    }


def _validate_score(score: float, *, name: str) -> None:
    if not 0 <= score <= 100:
        raise ValueError(f"{name} must be between 0 and 100.")
