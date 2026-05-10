import uvicorn
from fastapi import FastAPI

from app.configs.config import settings
from app.configs.cors import setup_cors
from app.health.health_controller import router as health_router
from app.proxy.routes import router as proxy_router


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        debug=settings.app_debug,
    )

    setup_cors(app)

    app.include_router(health_router)
    app.include_router(proxy_router)

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