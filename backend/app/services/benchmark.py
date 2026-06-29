from __future__ import annotations

import csv
import json
import math
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.services.baseline_matcher import calculate_skill_match
from app.services.embedding_matcher import SemanticModelUnavailable


REQUIRED_COLUMNS = (
    "pair_id",
    "candidate_group_id",
    "job_group_id",
    "resume_text",
    "job_description",
    "overall_label",
    "skills_label",
    "experience_label",
    "education_label",
    "label_reason",
    "label_source",
    "review_status",
)

ALLOWED_LABEL_SOURCES = {"human", "llm_assisted"}

LABEL_TO_SCORE = {
    0: 0.0,
    1: 33.33,
    2: 66.67,
    3: 100.0,
}

SemanticScorer = Callable[[str, str], float]


@dataclass(frozen=True)
class BenchmarkRow:
    pair_id: str
    candidate_group_id: str
    job_group_id: str
    resume_text: str
    job_description: str
    overall_label: int
    skills_label: int
    experience_label: int
    education_label: int
    label_reason: str
    label_source: str
    review_status: str


def load_benchmark_rows(path: Path) -> list[BenchmarkRow]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise ValueError("Dataset does not contain a CSV header.")

        missing_columns = [
            column
            for column in REQUIRED_COLUMNS
            if column not in reader.fieldnames
        ]
        if missing_columns:
            missing = ", ".join(missing_columns)
            raise ValueError(
                f"Dataset is missing required columns: {missing}."
            )

        rows: list[BenchmarkRow] = []
        seen_pair_ids: set[str] = set()

        for line_number, raw_row in enumerate(reader, start=2):
            if None in raw_row:
                raise ValueError(
                    f"Row {line_number} contains more values than columns."
                )

            values = {
                column: _clean_cell(raw_row.get(column))
                for column in REQUIRED_COLUMNS
            }

            if not any(values.values()):
                continue

            for column in (
                "pair_id",
                "candidate_group_id",
                "job_group_id",
                "resume_text",
                "job_description",
                "label_source",
                "review_status",
            ):
                if not values[column]:
                    raise ValueError(
                        f"Row {line_number} has an empty {column}."
                    )

            pair_id = values["pair_id"]
            if pair_id in seen_pair_ids:
                raise ValueError(
                    f"Row {line_number} has duplicate pair_id {pair_id!r}."
                )
            seen_pair_ids.add(pair_id)

            label_source = values["label_source"]
            if label_source not in ALLOWED_LABEL_SOURCES:
                allowed = ", ".join(sorted(ALLOWED_LABEL_SOURCES))
                raise ValueError(
                    f"Row {line_number} has unsupported label_source "
                    f"{label_source!r}; expected one of: {allowed}."
                )

            rows.append(
                BenchmarkRow(
                    pair_id=pair_id,
                    candidate_group_id=values["candidate_group_id"],
                    job_group_id=values["job_group_id"],
                    resume_text=values["resume_text"],
                    job_description=values["job_description"],
                    overall_label=_parse_label(
                        values["overall_label"],
                        column="overall_label",
                        line_number=line_number,
                    ),
                    skills_label=_parse_label(
                        values["skills_label"],
                        column="skills_label",
                        line_number=line_number,
                    ),
                    experience_label=_parse_label(
                        values["experience_label"],
                        column="experience_label",
                        line_number=line_number,
                    ),
                    education_label=_parse_label(
                        values["education_label"],
                        column="education_label",
                        line_number=line_number,
                    ),
                    label_reason=values["label_reason"],
                    label_source=label_source,
                    review_status=values["review_status"],
                )
            )

    if not rows:
        raise ValueError("Dataset contains no benchmark rows.")

    return rows


def evaluate_benchmark(
    rows: Sequence[BenchmarkRow],
    *,
    semantic_scorer: SemanticScorer | None = None,
) -> dict[str, Any]:
    if not rows:
        raise ValueError("At least one benchmark row is required.")

    targets: list[float] = []
    deterministic_scores: list[float] = []

    for row in rows:
        targets.append(LABEL_TO_SCORE[row.overall_label])

        result = calculate_skill_match(
            resume_text=row.resume_text,
            job_description=row.job_description,
        )
        deterministic_scores.append(float(result["match_score"]))

    semantic_status = "not_requested"
    semantic_scores: list[float] | None = None

    if semantic_scorer is not None:
        try:
            semantic_scores = [
                _validate_prediction(
                    semantic_scorer(
                        row.resume_text,
                        row.job_description,
                    ),
                    source="semantic",
                )
                for row in rows
            ]
        except SemanticModelUnavailable:
            semantic_status = "unavailable"
            semantic_scores = None
        else:
            semantic_status = "available"

    row_results: list[dict[str, object]] = []

    for index, row in enumerate(rows):
        row_results.append(
            {
                "pair_id": row.pair_id,
                "target_score": targets[index],
                "deterministic_score": deterministic_scores[index],
                "semantic_score": (
                    semantic_scores[index]
                    if semantic_scores is not None
                    else None
                ),
            }
        )

    return {
        "schema_version": "1.0",
        "sample_count": len(rows),
        "label_scale": {
            str(label): score
            for label, score in LABEL_TO_SCORE.items()
        },
        "deterministic": _build_metrics(
            deterministic_scores,
            targets,
        ),
        "semantic": (
            _build_metrics(semantic_scores, targets)
            if semantic_scores is not None
            else _empty_metrics(semantic_status)
        ),
        "rows": row_results,
    }


def write_benchmark_report(
    report: dict[str, Any],
    output_path: Path,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(
            report,
            indent=2,
            sort_keys=True,
            allow_nan=False,
        )
        + "\n",
        encoding="utf-8",
    )


def _build_metrics(
    predictions: Sequence[float],
    targets: Sequence[float],
) -> dict[str, object]:
    if len(predictions) != len(targets) or not predictions:
        raise ValueError(
            "Predictions and targets must have the same non-zero length."
        )

    mean_absolute_error = sum(
        abs(prediction - target)
        for prediction, target in zip(
            predictions,
            targets,
            strict=True,
        )
    ) / len(predictions)

    return {
        "status": "available",
        "sample_count": len(predictions),
        "mean_absolute_error": round(mean_absolute_error, 4),
        "pearson_correlation": _rounded_or_none(
            _pearson_correlation(predictions, targets)
        ),
        "spearman_correlation": _rounded_or_none(
            _pearson_correlation(
                _rank_values(predictions),
                _rank_values(targets),
            )
        ),
    }


def _empty_metrics(status: str) -> dict[str, object]:
    return {
        "status": status,
        "sample_count": 0,
        "mean_absolute_error": None,
        "pearson_correlation": None,
        "spearman_correlation": None,
    }


def _pearson_correlation(
    left: Sequence[float],
    right: Sequence[float],
) -> float | None:
    if len(left) != len(right) or len(left) < 2:
        return None

    left_mean = sum(left) / len(left)
    right_mean = sum(right) / len(right)

    numerator = sum(
        (left_value - left_mean) * (right_value - right_mean)
        for left_value, right_value in zip(left, right, strict=True)
    )
    left_variance = sum(
        (value - left_mean) ** 2
        for value in left
    )
    right_variance = sum(
        (value - right_mean) ** 2
        for value in right
    )

    denominator = math.sqrt(left_variance * right_variance)

    if denominator == 0:
        return None

    return numerator / denominator


def _rank_values(values: Sequence[float]) -> list[float]:
    ordered = sorted(
        enumerate(values),
        key=lambda item: item[1],
    )
    ranks = [0.0] * len(values)
    index = 0

    while index < len(ordered):
        end = index

        while (
            end + 1 < len(ordered)
            and ordered[end + 1][1] == ordered[index][1]
        ):
            end += 1

        average_rank = ((index + 1) + (end + 1)) / 2

        for position in range(index, end + 1):
            original_index = ordered[position][0]
            ranks[original_index] = average_rank

        index = end + 1

    return ranks


def _parse_label(
    value: str,
    *,
    column: str,
    line_number: int,
) -> int:
    try:
        label = int(value)
    except ValueError as exc:
        raise ValueError(
            f"Row {line_number} has a non-integer {column}."
        ) from exc

    if label not in LABEL_TO_SCORE:
        raise ValueError(
            f"Row {line_number} has {column} outside the 0 to 3 range."
        )

    return label


def _validate_prediction(score: float, *, source: str) -> float:
    numeric_score = float(score)

    if not math.isfinite(numeric_score) or not 0 <= numeric_score <= 100:
        raise ValueError(
            f"{source} score must be between 0 and 100."
        )

    return round(numeric_score, 2)


def _clean_cell(value: object) -> str:
    return value.strip() if isinstance(value, str) else ""


def _rounded_or_none(value: float | None) -> float | None:
    return None if value is None else round(value, 4)
