import logging

import httpx

from app.clients.recommendation.recommendation_dto import RecommendationRsDto
from app.clients.recommendation.recommendation_microservice_client import (
    RecommendationMicroserviceClient,
)
from app.clients.territory.territory_dto import TerritoryPointSearchRsDto
from app.clients.territory.territory_microservice_client import TerritoryMicroserviceClient
from app.service.territory_recommendation_dto import TerritoryPointSearchWithRecommendationRsDto

logger = logging.getLogger(__name__)


class TerritoryService:
    def __init__(self) -> None:
        self.territory_client = TerritoryMicroserviceClient()
        self.recommendation_client = RecommendationMicroserviceClient()

    async def get_by_point_with_recommendation(self, *, coord_x: float, coord_y: float, task_type: str, target: str | None = None) -> TerritoryPointSearchWithRecommendationRsDto | None:
        params = {
            "coord_x": coord_x,
            "coord_y": coord_y,
            "task_type": task_type,
            "target": target,
        }

        logger.info(
            "START TerritoryService::get_by_point_with_recommendation %s",
            params,
        )

        territory = await self.territory_client.get_related_objects_by_point(point_x=coord_x, point_y=coord_y)

        if territory is None:
            logger.info(
                "END TerritoryService::get_by_point_with_recommendation %s None",
                params,
            )
            return None

        recommendation = await self._safe_get_recommendation(coord_x=coord_x, coord_y=coord_y, task_type=task_type, target=target)

        result = self._merge_response(territory=territory, recommendation=recommendation)

        logger.info(
            "END TerritoryService::get_by_point_with_recommendation %s %s",
            params,
            result,
        )

        return result

    async def _safe_get_recommendation(self, *, coord_x: float, coord_y: float, task_type: str, target: str | None) -> RecommendationRsDto | None:
        try:
            return await self.recommendation_client.get_recommendation(point_x=coord_x, point_y=coord_y, task_type=task_type, target=target)
        except httpx.HTTPStatusError as exc:
            logger.warning(
                "Recommendation service returned error: status=%s body=%s",
                exc.response.status_code,
                exc.response.text,
            )
            return None
        except httpx.RequestError as exc:
            logger.warning(
                "Recommendation service request failed: %s",
                str(exc),
            )
            return None

    def _merge_response(self, *, territory: TerritoryPointSearchRsDto, recommendation: RecommendationRsDto | None) -> TerritoryPointSearchWithRecommendationRsDto:
        territory_data = territory.model_dump(mode="json")

        return TerritoryPointSearchWithRecommendationRsDto(
            **territory_data,
            recommendation=recommendation,
        )