import uvicorn
from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.configs.core.config import settings
from app.configs.core.cors import setup_cors
from app.configs.db.dependencies import get_db

from app.service.soil.soil_controller import router as soil_router


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        debug=settings.app_debug,
    )

    app.include_router(soil_router)

    setup_cors(app)

    @app.get("/health", tags=["system"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/health/db", tags=["system"])
    def health_db() -> dict[str, str]:
        db: Session = next(get_db())
        try:
            db.execute(text("SELECT 1"))
            return {"status": "ok"}
        finally:
            db.close()

    return app


app = create_app()

def main() -> None:
    uvicorn.run(
        "app.main:app",
        host= settings.app_host,
        port= settings.app_port,
        reload= settings.app_debug,
        log_level= settings.app_log_level,
    )


if __name__ == "__main__":
    main()