from fastapi import APIRouter, HTTPException, status

from app.service.recommendation.recommendation_dto import RecommendationRqDto, RecommendationRsDto
from app.service.recommendation.recommendation_dto_mapper import RecommendationDtoMapper
from app.service.recommendation.recommendation_service import RecommendationService


router = APIRouter(
    prefix="/api/v1/recommendations",
    tags=["recommendations"],
)


@router.post("", response_model=RecommendationRsDto)
async def create_recommendation(request: RecommendationRqDto):

    service = RecommendationService()

    result = await service.get_recommendation(point_x= request.point_x, point_y= request.point_y, task_type= request.task_type, target= request.target)

    if result is None:
        raise HTTPException(status_code=404, detail="Territory not found")

    return RecommendationDtoMapper.to_rs_dto(result)