import uvicorn
from fastapi import FastAPI

from app.core.config import settings
from app.core.cors import setup_cors
from app.service.auth.controllers import auth_controller
from app.service.users.controllers import user_controller
from app.service.file_metadata.file_metadata_controller import router as file_metadata_controller

app = FastAPI(title= settings.app_name)

setup_cors(app)

app.include_router(user_controller.router)
app.include_router(auth_controller.router)
app.include_router(file_metadata_controller)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host= settings.app_host,
        port= settings.app_port,
    )