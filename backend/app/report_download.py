from __future__ import annotations

import json
from datetime import date
from typing import Any

from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import Response

router = APIRouter()


def _mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _format_list(value: Any) -> str:
    if not isinstance(value, list):
        return "- None"

    items = [str(item).strip() for item in value if str(item).strip()]
    return "\n".join(f"- {item}" for item in items) or "- None"


def _format_questions(value: Any) -> str:
    if not isinstance(value, list) or not value:
        return "- None"

    formatted: list[str] = []

    for index, raw_item in enumerate(value, start=1):
        item = _mapping(raw_item)
        category = str(item.get("category", "general")).replace("_", " ")
        question = str(item.get("question", "Question unavailable"))
        outline = str(
            item.get("answer_outline", "No answer outline provided.")
        )

        formatted.append(
            "\n".join(
                [
                    f"{index}. [{category}] {question}",
                    f"   Answer outline: {outline}",
                ]
            )
        )

    return "\n\n".join(formatted)


def _format_evaluation(value: Any) -> str:
    evaluation = _mapping(value)

    if not evaluation:
        return "Not included in this report payload."

    deterministic_score = evaluation.get("deterministic_score", "—")
    interpretation = str(
        evaluation.get("interpretation", "Not provided.")
    )
    lines = [
        f"Explicit skill coverage: {deterministic_score}%",
    ]

    if evaluation.get("status") == "available":
        semantic_score = evaluation.get("semantic_score", "—")
        score_gap = evaluation.get("score_gap", "—")
        category = str(
            evaluation.get("gap_category", "unknown")
        ).replace("_", " ")

        lines.extend(
            [
                f"Semantic similarity: {semantic_score}%",
                f"Score difference: {score_gap} points",
                f"Difference category: {category}",
            ]
        )
    else:
        lines.append("Semantic comparison: unavailable")

    lines.append(f"Interpretation: {interpretation}")
    return "\n".join(lines)


def build_analysis_report(payload: dict[str, Any]) -> str:
    assessment = _mapping(payload.get("assessment"))
    result = _mapping(payload.get("result"))
    semantic = _mapping(payload.get("semantic"))

    if semantic.get("status") == "available":
        semantic_summary = f"{semantic.get('score', '—')}%"
    else:
        note = semantic.get("note", "No semantic score available.")
        semantic_summary = f"Unavailable — {note}"

    return "\n".join(
        [
            "CareerCraft AI Analysis Report",
            "================================",
            f"Generated: {date.today().isoformat()}",
            "",
            "Scores",
            "------",
            f"Overall match: {assessment.get('overall_score', '—')}%",
            f"Skill coverage: {assessment.get('skill_score', '—')}%",
            f"Resume structure: {assessment.get('structure_score', '—')}%",
            f"Semantic similarity: {semantic_summary}",
            "",
            "Matched skills",
            "--------------",
            _format_list(result.get("matched_skills")),
            "",
            "Missing skills",
            "--------------",
            _format_list(result.get("missing_skills")),
            "",
            "Detected resume sections",
            "------------------------",
            _format_list(assessment.get("found_sections")),
            "",
            "Missing resume sections",
            "-----------------------",
            _format_list(assessment.get("missing_sections")),
            "",
            "Recommended next steps",
            "----------------------",
            _format_list(assessment.get("recommendations")),
            "",
            "Interview practice",
            "------------------",
            _format_questions(payload.get("interview_questions")),
            "",
            "Methodology",
            "-----------",
            str(payload.get("methodology", "Not provided.")),
            "",
        ]
    )


@router.post("/api/report")
async def download_analysis_report(payload: str = Form(...)) -> Response:
    try:
        parsed_payload = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=400,
            detail="The report payload is not valid JSON.",
        ) from exc

    if not isinstance(parsed_payload, dict):
        raise HTTPException(
            status_code=422,
            detail="The report payload must be a JSON object.",
        )

    if not isinstance(parsed_payload.get("assessment"), dict):
        raise HTTPException(
            status_code=422,
            detail="The report payload is missing assessment data.",
        )

    report = build_analysis_report(parsed_payload)
    filename = f"careercraft-analysis-{date.today().isoformat()}.txt"

    return Response(
        content=report,
        media_type="text/plain; charset=utf-8",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Cache-Control": "no-store",
        },
    )
