import csv
import json
from pathlib import Path

import pytest

from app.services.benchmark import (
    REQUIRED_COLUMNS,
    evaluate_benchmark,
    load_benchmark_rows,
    write_benchmark_report,
)
from app.services.embedding_matcher import SemanticModelUnavailable


def _valid_row(**overrides: str) -> dict[str, str]:
    row = {
        "pair_id": "pair-1",
        "candidate_group_id": "candidate-1",
        "job_group_id": "job-1",
        "resume_text": "Python FastAPI backend engineer",
        "job_description": "Python FastAPI backend role",
        "overall_label": "3",
        "skills_label": "3",
        "experience_label": "2",
        "education_label": "2",
        "label_reason": "Strong skill alignment.",
        "label_source": "human",
        "review_status": "reviewed",
    }
    row.update(overrides)
    return row


def _write_dataset(
    path: Path,
    rows: list[dict[str, str]],
    *,
    fieldnames: tuple[str, ...] = REQUIRED_COLUMNS,
) -> None:
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def test_benchmark_evaluates_deterministic_and_semantic_scores(
    tmp_path: Path,
) -> None:
    dataset = tmp_path / "dataset.csv"
    _write_dataset(
        dataset,
        [
            _valid_row(),
            _valid_row(
                pair_id="pair-2",
                candidate_group_id="candidate-2",
                job_group_id="job-2",
                resume_text="React frontend developer",
                job_description="Python FastAPI backend role",
                overall_label="0",
                skills_label="0",
                experience_label="0",
                education_label="1",
            ),
        ],
    )

    rows = load_benchmark_rows(dataset)

    def semantic_scorer(resume: str, _: str) -> float:
        return 90.0 if "Python" in resume else 10.0

    report = evaluate_benchmark(
        rows,
        semantic_scorer=semantic_scorer,
    )

    assert report["sample_count"] == 2
    assert report["deterministic"] == {
        "status": "available",
        "sample_count": 2,
        "mean_absolute_error": 0.0,
        "pearson_correlation": 1.0,
        "spearman_correlation": 1.0,
    }
    assert report["semantic"] == {
        "status": "available",
        "sample_count": 2,
        "mean_absolute_error": 10.0,
        "pearson_correlation": 1.0,
        "spearman_correlation": 1.0,
    }
    assert report["rows"][0]["pair_id"] == "pair-1"
    assert "resume_text" not in report["rows"][0]


def test_dataset_rejects_missing_columns(tmp_path: Path) -> None:
    dataset = tmp_path / "missing-columns.csv"
    _write_dataset(
        dataset,
        [{"pair_id": "pair-1"}],
        fieldnames=("pair_id",),
    )

    with pytest.raises(ValueError, match="missing required columns"):
        load_benchmark_rows(dataset)


def test_dataset_rejects_invalid_labels(tmp_path: Path) -> None:
    dataset = tmp_path / "invalid-label.csv"
    _write_dataset(
        dataset,
        [_valid_row(overall_label="4")],
    )

    with pytest.raises(ValueError, match="outside the 0 to 3 range"):
        load_benchmark_rows(dataset)


def test_dataset_rejects_duplicate_pair_ids(tmp_path: Path) -> None:
    dataset = tmp_path / "duplicates.csv"
    _write_dataset(
        dataset,
        [
            _valid_row(),
            _valid_row(
                candidate_group_id="candidate-2",
                job_group_id="job-2",
            ),
        ],
    )

    with pytest.raises(ValueError, match="duplicate pair_id"):
        load_benchmark_rows(dataset)


def test_dataset_rejects_empty_files(tmp_path: Path) -> None:
    dataset = tmp_path / "empty.csv"
    _write_dataset(dataset, [])

    with pytest.raises(ValueError, match="no benchmark rows"):
        load_benchmark_rows(dataset)


def test_benchmark_handles_unavailable_semantic_model(
    tmp_path: Path,
) -> None:
    dataset = tmp_path / "dataset.csv"
    _write_dataset(dataset, [_valid_row()])
    rows = load_benchmark_rows(dataset)

    def unavailable_scorer(_: str, __: str) -> float:
        raise SemanticModelUnavailable("Model unavailable.")

    report = evaluate_benchmark(
        rows,
        semantic_scorer=unavailable_scorer,
    )

    assert report["semantic"]["status"] == "unavailable"
    assert report["semantic"]["sample_count"] == 0
    assert report["rows"][0]["semantic_score"] is None


def test_report_writer_is_reproducible(tmp_path: Path) -> None:
    dataset = tmp_path / "dataset.csv"
    _write_dataset(dataset, [_valid_row()])
    report = evaluate_benchmark(load_benchmark_rows(dataset))

    first_output = tmp_path / "first.json"
    second_output = tmp_path / "second.json"

    write_benchmark_report(report, first_output)
    write_benchmark_report(report, second_output)

    assert first_output.read_bytes() == second_output.read_bytes()
    assert json.loads(first_output.read_text())["schema_version"] == "1.0"


def test_benchmark_rejects_invalid_semantic_scores(
    tmp_path: Path,
) -> None:
    dataset = tmp_path / "dataset.csv"
    _write_dataset(dataset, [_valid_row()])
    rows = load_benchmark_rows(dataset)

    with pytest.raises(
        ValueError,
        match="semantic score must be between 0 and 100",
    ):
        evaluate_benchmark(
            rows,
            semantic_scorer=lambda _resume, _job: 120.0,
        )
