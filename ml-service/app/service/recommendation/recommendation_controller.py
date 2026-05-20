from uuid import UUID
from fastapi import APIRouter, HTTPException, Path, status

from app.service.recommendation.recommendation_dto import (
    FeedbackRqDto,
    FeedbackRsDto,
    RecommendationRqDto,
    RecommendationRsDto,
)
from app.service.recommendation.recommendation_dto_mapper import RecommendationDtoMapper
from app.service.recommendation.recommendation_service import RecommendationService


router = APIRouter(
    prefix="/api/v1/recommendations",
    tags=["recommendations"],
)


@router.post("", response_model=RecommendationRsDto)
async def create_recommendation(request: RecommendationRqDto):
    service = RecommendationService()

    result = await service.get_recommendation(
        point_x=request.point_x,
        point_y=request.point_y,
        task_type=request.task_type,
        target=request.target,
    )
    if result is None:
        raise HTTPException(status_code=404, detail="Territory not found")

    return RecommendationDtoMapper.to_rs_dto(result)


@router.post("/{request_id}/feedback", response_model=FeedbackRsDto)
async def set_recommendation_feedback(
    request_id: UUID = Path(..., description="UUID запроса рекомендации"),
    body: FeedbackRqDto = None,
):
    """Оценить рекомендацию от 1 до 10."""
    if body is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request body is required",
        )

    service = RecommendationService()

    result = await service.set_feedback(
        request_id=request_id,
        rating=body.rating,
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recommendation request not found: {request_id}",
        )

    return RecommendationDtoMapper.feedback_to_rs_dto(result)


@router.get("/{request_id}/feedback", response_model=FeedbackRsDto)
async def get_recommendation_feedback(
    request_id: UUID = Path(..., description="UUID запроса рекомендации"),
):
    """Получить текущую оценку рекомендации (если есть)."""
    service = RecommendationService()

    result = await service.get_feedback(request_id=request_id)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recommendation request not found: {request_id}",
        )

    return RecommendationDtoMapper.feedback_to_rs_dto(result)
