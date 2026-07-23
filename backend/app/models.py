from typing import Literal

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    resume_text: str = Field(min_length=30)
    job_description: str = Field(min_length=30)
    include_semantic: bool = False


class SkillMatch(BaseModel):
    resume_skills: list[str]
    required_skills: list[str]
    matched_skills: list[str]
    missing_skills: list[str]
    match_score: float


class AnalysisAssessment(BaseModel):
    overall_score: float
    skill_score: float
    structure_score: float
    found_sections: list[str]
    missing_sections: list[str]
    recommendations: list[str]


class SemanticMatch(BaseModel):
    status: Literal["available", "unavailable", "not_requested"]
    score: float | None = Field(default=None, ge=0, le=100)
    model: str
    note: str


class EvaluationComparison(BaseModel):
    status: Literal["available", "unavailable", "not_requested"]
    deterministic_score: float = Field(ge=0, le=100)
    semantic_score: float | None = Field(default=None, ge=0, le=100)
    score_gap: float | None = Field(default=None, ge=0, le=100)
    gap_category: Literal["close", "moderate", "wide", "not_available"]
    interpretation: str




class InterviewQuestion(BaseModel):
    category: Literal["technical", "learning_gap", "behavioral"]
    question: str
    answer_outline: str


class AnalyzeResponse(BaseModel):
    result: SkillMatch
    assessment: AnalysisAssessment
    semantic: SemanticMatch
    evaluation: EvaluationComparison
    interview_questions: list[InterviewQuestion]
    methodology: str


class ResumeParseResponse(BaseModel):
    filename: str
    character_count: int
    word_count: int
    text: str
    sections: dict[str, str]
