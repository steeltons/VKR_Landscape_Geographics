import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.concurrency import run_in_threadpool

from app.configs.config import settings
from app.service.health.health_controller import router as health_router
from app.ml.models.model_registry import get_model_registry
from app.service.model.model_controller import router as model_router
from app.service.recommendation.recommendation_controller import router as recommendation_router


logging.basicConfig(
    level=logging.DEBUG if settings.app_debug else logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("START application lifespan startup")

    try:
        await run_in_threadpool(get_model_registry().preload_current_model)
    except Exception as exc:
        logger.exception("Failed to preload ML model on startup: %s", str(exc))

        if settings.model_fail_fast_on_startup:
            raise

    logger.info("END application lifespan startup")

    yield

    logger.info("START application lifespan shutdown")
    logger.info("END application lifespan shutdown")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        debug=settings.app_debug,
        lifespan=lifespan,
    )

    app.include_router(health_router)
    app.include_router(recommendation_router)
    app.include_router(model_router)

    return app


app = create_app()


def main() -> None:
    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.app_debug,
        log_level=settings.debug_level,
    )


if __name__ == "__main__":
    main()