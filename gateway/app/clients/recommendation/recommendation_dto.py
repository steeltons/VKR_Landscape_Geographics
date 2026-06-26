from pydantic import BaseModel, Field


class RecommendationRqDto(BaseModel):
    task_type: str = Field(min_length=1)
    point_x: float
    point_y: float
    target: str | None = None


class EvidenceRsDto(BaseModel):
    object_type: str
    object_id: int
    title: str
    api_path: str
    impact: str
    factor: str
    reason: str


class ExplanationRsDto(BaseModel):
    summary: str
    reasons: list[str]
    warnings: list[str]
    evidence: list[EvidenceRsDto]


class RecommendationRsDto(BaseModel):
    score: float
    level: str
    recommendation: str
    explanation: ExplanationRsDto