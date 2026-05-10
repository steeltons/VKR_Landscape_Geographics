import logging

import uvicorn
from fastapi import FastAPI

from app.service.recommendation.recommendation_controller import router as recommendation_router
from app.service.health.health_controller import router as health_router
from app.configs.config import settings


logging.basicConfig(
    level=logging.DEBUG if settings.app_debug else logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        debug=settings.app_debug,
    )

    app.include_router(health_router)
    app.include_router(recommendation_router)

    return app


app = create_app()


def main() -> None:
    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.app_debug,
        log_level="debug" if settings.app_debug else "info",
    )


if __name__ == "__main__":
    main()