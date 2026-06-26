from fastapi import FastAPI

from app.models import AnalyzeRequest, AnalyzeResponse, SkillMatch
from app.services.baseline_matcher import calculate_skill_match


app = FastAPI(
    title="CareerCraft AI API",
    version="0.1.0",
    description="Explainable resume-to-job matching and interview intelligence.",
)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "careercraft-ai",
        "version": "0.1.0",
    }


@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze(payload: AnalyzeRequest) -> AnalyzeResponse:
    raw_result = calculate_skill_match(
        resume_text=payload.resume_text,
        job_description=payload.job_description,
    )

    return AnalyzeResponse(
        result=SkillMatch(**raw_result),
        methodology=(
            "Deterministic skill-overlap baseline. Embedding retrieval, "
            "section-aware scoring and LLM explanations will be added next."
        ),
    )
