from app.ml.pipelines.recommendation_pipeline import RecommendationPipeline
from app.persistence.dictionary_microservice_client import DictionaryMicroserviceClient


class RecommendationService:
    def __init__(self) -> None:
        self.client = DictionaryMicroserviceClient()
        self.pipeline = RecommendationPipeline()

    async def get_recommendation(self, *, point_x: float, point_y: float, task_type: str, target: str | None) -> dict | None:

        data = await self.client.get_territories_by_point(point_x=point_x, point_y=point_y)

        if data is None:
            return None

        result = self.pipeline.run(data= data, task_type= task_type, target=target)

        return result