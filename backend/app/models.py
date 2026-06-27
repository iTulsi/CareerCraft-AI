from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    resume_text: str = Field(min_length=30)
    job_description: str = Field(min_length=30)


class SkillMatch(BaseModel):
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


class AnalyzeResponse(BaseModel):
    result: SkillMatch
    assessment: AnalysisAssessment
    methodology: str


class ResumeParseResponse(BaseModel):
    filename: str
    character_count: int
    word_count: int
    text: str
    sections: dict[str, str]
