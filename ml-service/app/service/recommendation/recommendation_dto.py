from pydantic import BaseModel, Field


class RecommendationRqDto(BaseModel):
    task_type: str = Field(min_length=1)
    point_x: float
    point_y: float
    target: str | None = None


class ExplanationRsDto(BaseModel):
    summary: str
    reasons: list[str]
    warnings: list[str]


class RecommendationRsDto(BaseModel):
    score: float
    explanation: ExplanationRsDto