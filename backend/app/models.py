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




class JobRequirements(BaseModel):
    experience_requirements: list[str]
    seniority_signals: list[str]
    education_requirements: list[str]
    work_arrangements: list[str]


class ResumeQuality(BaseModel):
    word_count: int = Field(ge=0)
    bullet_count: int = Field(ge=0)
    action_oriented_statements: int = Field(ge=0)
    quantified_statements: int = Field(ge=0)
    quantified_statement_ratio: float = Field(ge=0, le=100)
    suggestions: list[str]


class SkillEvidence(BaseModel):
    skill: str
    sections: list[str]
    snippet: str | None
    quantified: bool


class SkillPriority(BaseModel):
    skill: str
    mentions: int = Field(ge=1)
    priority: Literal["high", "medium", "low"]
    reason: str


class InterviewQuestion(BaseModel):
    category: Literal["technical", "learning_gap", "behavioral"]
    question: str
    answer_outline: str


class AnalyzeResponse(BaseModel):
    result: SkillMatch
    assessment: AnalysisAssessment
    skill_priorities: list[SkillPriority]
    skill_evidence: list[SkillEvidence]
    resume_quality: ResumeQuality
    job_requirements: JobRequirements
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
