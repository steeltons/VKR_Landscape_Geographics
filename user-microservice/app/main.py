import uvicorn
from fastapi import FastAPI

from app.core.config import settings
from app.service.users import user_controller

app = FastAPI(title= settings.app_name)

app.include_router(user_controller.router)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host= settings.app_host,
        port= settings.app_port,
    )