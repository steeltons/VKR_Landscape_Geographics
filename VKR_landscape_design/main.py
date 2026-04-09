from typing import Optional

import uvicorn

from controllers import UserController
from controllers import TerritorieController
from controllers import CoordsController
from controllers import LandscapeController
from controllers import SoilController
from controllers import GroundController
from controllers import PlantController
from controllers import ReliefController
from controllers import FoundationController
from controllers import WaterController
from controllers import ClimatController
from controllers import PictureController
from controllers import ConnectionLandscapesSoilsController
from controllers import ConnectionLandscapesGroundsController
from controllers import ConnectionLandscapesPlantsController
from controllers import ConnectionLandscapesReliefsController
from controllers import ConnectionLandscapesFoundationsController
from controllers import ConnectionLandscapesWatersController
from controllers import ConnectionLandscapesClimatsController
from fastapi import FastAPI
from pydantic import BaseModel

from core.config import settings
from core.cors import setup_cors

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

app = FastAPI(title= settings.app_name)
setup_cors(app)

app.include_router(UserController.router)
app.include_router(TerritorieController.router)
app.include_router(CoordsController.router)
app.include_router(LandscapeController.router)
app.include_router(SoilController.router)
app.include_router(GroundController.router)
app.include_router(PlantController.router)
app.include_router(ReliefController.router)
app.include_router(FoundationController.router)
app.include_router(WaterController.router)
app.include_router(ClimatController.router)
app.include_router(PictureController.router)
app.include_router(ConnectionLandscapesSoilsController.router)
app.include_router(ConnectionLandscapesGroundsController.router)
app.include_router(ConnectionLandscapesPlantsController.router)
app.include_router(ConnectionLandscapesReliefsController.router)
app.include_router(ConnectionLandscapesFoundationsController.router)
app.include_router(ConnectionLandscapesWatersController.router)
app.include_router(ConnectionLandscapesClimatsController.router)

if __name__ == '__main__':
    uvicorn.run(
        app,
        host= settings.app_host,
        port= settings.app_port,
        log_level= settings.app_debug,
    )