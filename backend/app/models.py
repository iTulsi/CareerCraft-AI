from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    resume_text: str = Field(min_length=30)
    job_description: str = Field(min_length=30)


class SkillMatch(BaseModel):
    matched_skills: list[str]
    missing_skills: list[str]
    match_score: float


class AnalyzeResponse(BaseModel):
    result: SkillMatch
    methodology: str
