import httpx

from app.configs.config import settings

class DictionaryMicroserviceClient:

    __TERRITORIES_BY_POINT_PATH = '/api/v1/territories/by-point/related-objects'

    def __init__(self):
        self.base_url = settings.dictionary_microservice_base_url
        self.timeout = settings.dictionary_microservice_timeout

    async def get_territories_by_point(self, *, point_x, point_y) -> dict | None:
        url = self.base_url + self.__TERRITORIES_BY_POINT_PATH

        async with httpx.AsyncClient(timeout= self.timeout) as client:
            response = await client.get(url, params={'point_x': point_x, 'point_y': point_y})

            if response.status_code == 404:
                return None

            response.raise_for_status()
            return response.json()