# main.py

from typing import Optional

from starlette.middleware.cors import CORSMiddleware

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

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

app = FastAPI()

origins = [
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

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