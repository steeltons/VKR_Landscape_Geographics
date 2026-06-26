import logging

import httpx

from app.clients.territory.territory_dto import TerritoryPointSearchRsDto
from app.configs.config import settings

logger = logging.getLogger(__name__)


class TerritoryMicroserviceClient:

    def __init__(self) -> None:
        self.base_url = settings.dictionary_service_url
        self.timeout = settings.request_timeout_seconds

    async def get_related_objects_by_point(self, *, point_x: float, point_y: float) -> TerritoryPointSearchRsDto | None:
        url = f"{self.base_url}/api/v1/territories/by-point/related-objects"

        params = {
            "point_x": point_x,
            "point_y": point_y,
        }

        logger.debug(
            "START DictionaryMicroserviceClient::get_related_objects_by_point %s",
            params,
        )

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                url,
                params=params,
            )

        if response.status_code == 404:
            logger.debug(
                "END DictionaryMicroserviceClient::get_related_objects_by_point %s None",
                params,
            )
            return None

        response.raise_for_status()

        result = TerritoryPointSearchRsDto.model_validate(response.json())

        logger.debug(
            "END DictionaryMicroserviceClient::get_related_objects_by_point %s %s",
            params,
            result,
        )

        return result