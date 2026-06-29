import csv
import json
from pathlib import Path

from app.benchmark import main
from app.services.benchmark import REQUIRED_COLUMNS


def _write_dataset(path: Path) -> None:
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
        "label_reason": "Strong alignment.",
        "label_source": "human",
        "review_status": "reviewed",
    }

    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=REQUIRED_COLUMNS)
        writer.writeheader()
        writer.writerow(row)


def test_cli_writes_benchmark_report(
    tmp_path: Path,
    capsys,
) -> None:
    dataset = tmp_path / "dataset.csv"
    output = tmp_path / "report.json"
    _write_dataset(dataset)

    exit_code = main(
        [
            "--dataset",
            str(dataset),
            "--output",
            str(output),
        ]
    )

    assert exit_code == 0
    assert output.exists()

    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["sample_count"] == 1
    assert report["deterministic"]["status"] == "available"
    assert report["semantic"]["status"] == "not_requested"

    captured = capsys.readouterr()
    assert "Benchmark completed for 1 pairs" in captured.out


def test_cli_supports_semantic_evaluation(
    tmp_path: Path,
    monkeypatch,
) -> None:
    dataset = tmp_path / "dataset.csv"
    output = tmp_path / "report.json"
    _write_dataset(dataset)

    monkeypatch.setattr(
        "app.benchmark.calculate_semantic_similarity",
        lambda _resume, _job: 82.5,
    )

    exit_code = main(
        [
            "--dataset",
            str(dataset),
            "--output",
            str(output),
            "--include-semantic",
        ]
    )

    assert exit_code == 0

    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["semantic"]["status"] == "available"
    assert report["rows"][0]["semantic_score"] == 82.5


def test_cli_reports_invalid_dataset(
    tmp_path: Path,
    capsys,
) -> None:
    dataset = tmp_path / "invalid.csv"
    output = tmp_path / "report.json"
    dataset.write_text("pair_id\npair-1\n", encoding="utf-8")

    exit_code = main(
        [
            "--dataset",
            str(dataset),
            "--output",
            str(output),
        ]
    )

    assert exit_code == 1
    assert not output.exists()

    captured = capsys.readouterr()
    assert "Benchmark failed:" in captured.err
    assert "missing required columns" in captured.err
