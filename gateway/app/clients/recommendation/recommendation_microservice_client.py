import logging

import httpx

from app.configs.config import settings
from app.clients.recommendation.recommendation_dto import RecommendationRsDto


logger = logging.getLogger(__name__)


class RecommendationMicroserviceClient:
    def __init__(self) -> None:
        self.base_url = settings.ml_service_url
        self.timeout = settings.request_timeout_seconds

    async def get_recommendation(self, *, point_x: float, point_y: float, task_type: str, target: str | None = None) -> RecommendationRsDto | None:
        url = f"{self.base_url}/api/v1/recommendations"

        payload = {
            "point_x": point_x,
            "point_y": point_y,
            "task_type": task_type,
            "target": target,
        }

        logger.info(
            "START RecommendationMicroserviceClient::get_recommendation %s",
            payload,
        )

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                url,
                json=payload,
            )

        if response.status_code == 404:
            logger.info(
                "END RecommendationMicroserviceClient::get_recommendation %s None",
                payload,
            )
            return None

        response.raise_for_status()

        result = RecommendationRsDto.model_validate(response.json())

        logger.info(
            "END RecommendationMicroserviceClient::get_recommendation %s %s",
            payload,
            result,
        )

        return result