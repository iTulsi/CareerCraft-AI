from app.report_download import router as report_download_router
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.models import (
    AnalyzeRequest,
    AnalysisAssessment,
    AnalyzeResponse,
    InterviewQuestion,
    ResumeParseResponse,
    SemanticMatch,
    SkillMatch,
)
from app.services.analysis_service import calculate_resume_assessment
from app.services.interview_questions import build_interview_questions
from app.services.document_parser import (
    DocumentParseError,
    MAX_FILE_SIZE_BYTES,
    extract_text,
)
from app.services.embedding_matcher import (
    MODEL_NAME,
    SemanticModelUnavailable,
    calculate_semantic_similarity,
)
from app.services.section_parser import detect_sections


PROJECT_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_DIR = PROJECT_ROOT / "frontend"

app = FastAPI(
    title="CareerCraft AI API",
    version="0.3.0",
    description="Explainable resume-to-job matching and interview intelligence.",
)

app.include_router(report_download_router)

app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR / "static"),
    name="static",
)


@app.get("/", include_in_schema=False)
def home() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "careercraft-ai",
        "version": "0.3.0",
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
    skill_match, assessment = calculate_resume_assessment(
        resume_text=payload.resume_text,
        job_description=payload.job_description,
    )
    semantic = _semantic_result(payload)
    interview_questions = build_interview_questions(
        matched_skills=list(skill_match["matched_skills"]),
        missing_skills=list(skill_match["missing_skills"]),
        found_sections=list(assessment["found_sections"]),
    )

    return AnalyzeResponse(
        result=SkillMatch(**skill_match),
        assessment=AnalysisAssessment(**assessment),
        semantic=semantic,
        interview_questions=[
            InterviewQuestion(**question)
            for question in interview_questions
        ],
        methodology=(
            "Deterministic heuristic, not an employer ATS score: "
            "75% job-skill coverage and 25% resume-section coverage. "
            "Semantic similarity is shown separately and is not included "
            "in the overall score until it is validated on labelled data."
        ),
    )


def _semantic_result(payload: AnalyzeRequest) -> SemanticMatch:
    if not payload.include_semantic:
        return SemanticMatch(
            status="not_requested",
            score=None,
            model=MODEL_NAME,
            note="Semantic comparison was not requested.",
        )

    try:
        score = calculate_semantic_similarity(
            resume_text=payload.resume_text,
            job_description=payload.job_description,
        )
    except SemanticModelUnavailable:
        return SemanticMatch(
            status="unavailable",
            score=None,
            model=MODEL_NAME,
            note=(
                "Install backend/requirements-ml.txt to enable local "
                "semantic comparison."
            ),
        )

    return SemanticMatch(
        status="available",
        score=score,
        model=MODEL_NAME,
        note=(
            "Cosine similarity from a pretrained embedding model; "
            "this is not a hiring probability."
        ),
    )
