from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from app.services.benchmark import (
    evaluate_benchmark,
    load_benchmark_rows,
    write_benchmark_report,
)
from app.services.embedding_matcher import calculate_semantic_similarity


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Evaluate CareerCraft matchers against a labelled CSV dataset."
        )
    )
    parser.add_argument(
        "--dataset",
        required=True,
        type=Path,
        help="Path to the labelled annotation CSV.",
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Path for the generated benchmark JSON report.",
    )
    parser.add_argument(
        "--include-semantic",
        action="store_true",
        help="Evaluate the optional sentence-transformer matcher.",
    )
    args = parser.parse_args(argv)

    try:
        rows = load_benchmark_rows(args.dataset)
        report = evaluate_benchmark(
            rows,
            semantic_scorer=(
                calculate_semantic_similarity
                if args.include_semantic
                else None
            ),
        )
        write_benchmark_report(report, args.output)
    except (OSError, ValueError) as exc:
        print(f"Benchmark failed: {exc}", file=sys.stderr)
        return 1

    print(
        f"Benchmark completed for {report['sample_count']} pairs. "
        f"Report written to {args.output}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
