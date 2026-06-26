from fastapi import FastAPI, File, HTTPException, UploadFile

from app.models import (
    AnalyzeRequest,
    AnalyzeResponse,
    ResumeParseResponse,
    SkillMatch,
)
from app.services.baseline_matcher import calculate_skill_match
from app.services.document_parser import (
    DocumentParseError,
    MAX_FILE_SIZE_BYTES,
    extract_text,
)
from app.services.section_parser import detect_sections


app = FastAPI(
    title="CareerCraft AI API",
    version="0.2.0",
    description="Explainable resume-to-job matching and interview intelligence.",
)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "careercraft-ai",
        "version": "0.2.0",
    }


@app.post("/api/resume/parse", response_model=ResumeParseResponse)
async def parse_resume(
    file: UploadFile = File(...),
) -> ResumeParseResponse:
    filename = file.filename or "resume"
    content = await file.read(MAX_FILE_SIZE_BYTES + 1)

    try:
        if len(content) > MAX_FILE_SIZE_BYTES:
            raise DocumentParseError("The uploaded file exceeds the 5 MB limit.")

        text = extract_text(filename=filename, content=content)
    except DocumentParseError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return ResumeParseResponse(
        filename=filename,
        character_count=len(text),
        word_count=len(text.split()),
        text=text,
        sections=detect_sections(text),
    )


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
