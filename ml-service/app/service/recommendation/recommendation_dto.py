from uuid import UUID

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
    request_id: UUID
    score: float
    level: str
    recommendation: str
    explanation: ExplanationRsDto


# --- Feedback DTOs ---


class FeedbackRqDto(BaseModel):
    rating: int = Field(ge=1, le=10, description="Оценка рекомендации от 1 до 10")


class FeedbackRsDto(BaseModel):
    request_id: UUID
    rating: int
    rated_at: str
    message: str = "Спасибо за оценку!"
