import logging
import uuid

from starlette.concurrency import run_in_threadpool

from app.ml.models.model_registry import get_model_registry
from app.ml.pipelines.recommendation_pipeline import RecommendationPipeline
from app.persistence.dictionary_microservice_client import DictionaryMicroserviceClient
from app.persistence.recommendation_feedback_repository import RecommendationFeedbackRepository


logger = logging.getLogger(__name__)


class RecommendationService:
    def __init__(self) -> None:
        self.client = DictionaryMicroserviceClient()
        self.pipeline = RecommendationPipeline()
        self.repository = RecommendationFeedbackRepository()
        self.model_registry = get_model_registry()

    async def get_recommendation(
        self,
        *,
        point_x: float,
        point_y: float,
        task_type: str,
        target: str | None,
    ) -> dict | None:
        logger.info(
            "START RecommendationService::get_recommendation point=(%s, %s) task=%s target=%s",
            point_x,
            point_y,
            task_type,
            target,
        )

        # 1. Get data from dictionary-service
        data = await self.client.get_territories_by_point(
            point_x=point_x,
            point_y=point_y,
        )

        if data is None:
            logger.info(
                "END RecommendationService::get_recommendation territory_not_found "
                "point=(%s, %s)",
                point_x,
                point_y,
            )
            return None

        # 2. Extract territory and landscape info for the feedback record
        territory = data.get("territory") or {}
        landscape = data.get("landscape") or {}
        territory_id = territory.get("id")
        landscape_id = landscape.get("id")

        # 3. Generate a unique request id
        request_id = uuid.uuid4()

        # 4. Get current model version from artifact storage
        try:
            model_version = await run_in_threadpool(
                self.model_registry.artifact_storage.get_current_model_version,
            )
        except Exception:
            model_version = "unknown"

        # 5. Create initial feedback record (rating=NULL, model_score=0 placeholder)
        await run_in_threadpool(
            self.repository.create,
            request_id=request_id,
            point_x=point_x,
            point_y=point_y,
            task_type=task_type,
            target=target,
            territory_id=territory_id,
            landscape_id=landscape_id,
            model_version=model_version,
            model_score=0.0,
            features=None,
        )

        # 6. Run ML pipeline
        result = self.pipeline.run(data=data, task_type=task_type, target=target)

        # 7. Update feedback record with actual model result
        score = float(result.get("score", 0.0))
        features = result.get("features", {})
        actual_model_version = result.get("model_version", model_version)

        await run_in_threadpool(
            self.repository.update_model_result,
            request_id=request_id,
            model_version=actual_model_version,
            model_score=score,
            features=features,
        )

        # 8. Attach request_id to result
        result["request_id"] = request_id

        logger.info(
            "END RecommendationService::get_recommendation request_id=%s score=%s",
            request_id,
            score,
        )

        return result

    async def get_feedback(
        self,
        *,
        request_id: uuid.UUID,
    ) -> dict | None:
        """Get feedback record by request_id."""
        logger.debug(
            "START RecommendationService::get_feedback request_id=%s",
            request_id,
        )

        entity = await run_in_threadpool(
            self.repository.get_by_request_id,
            request_id=request_id,
        )

        if entity is None:
            logger.debug(
                "END RecommendationService::get_feedback request_id=%s not_found",
                request_id,
            )
            return None

        result = {
            "request_id": entity.request_id,
            "rating": entity.rating,
            "rated_at": entity.rated_at.isoformat() if entity.rated_at else None,
        }

        logger.debug(
            "END RecommendationService::get_feedback request_id=%s rating=%s",
            request_id,
            entity.rating,
        )

        return result

    async def set_feedback(
        self,
        *,
        request_id: uuid.UUID,
        rating: int,
    ) -> dict | None:
        """Set user rating for a recommendation."""
        logger.info(
            "START RecommendationService::set_feedback request_id=%s rating=%s",
            request_id,
            rating,
        )

        entity = await run_in_threadpool(
            self.repository.update_rating,
            request_id=request_id,
            rating=rating,
        )

        if entity is None:
            logger.warning(
                "END RecommendationService::set_feedback request_id=%s not_found",
                request_id,
            )
            return None

        result = {
            "request_id": entity.request_id,
            "rating": entity.rating,
            "rated_at": entity.rated_at.isoformat() if entity.rated_at else "",
        }

        logger.info(
            "END RecommendationService::set_feedback request_id=%s rating=%s success",
            request_id,
            rating,
        )

        return result
