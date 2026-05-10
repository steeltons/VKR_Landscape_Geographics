import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.components.coordinates.coordinates_component import CoordinatesComponent
from app.service.coordinates.coordinates_dto import TerritoryCoordinatesRsDto
from app.service.coordinates.coordinates_dto_mapper import CoordinatesDtoMapper
from app.configs.db.dependencies import get_db


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/coordinates",
    tags=["coordinates"],
)


@router.get("", response_model=TerritoryCoordinatesRsDto)
def get_coordinates(
    db: Session = Depends(get_db),
) -> TerritoryCoordinatesRsDto:
    logger.debug("START CoordinatesController::get_coordinates")

    component = CoordinatesComponent(db)
    result = CoordinatesDtoMapper.to_rs_dto(
        component.get_all_coordinates(),
    )

    logger.debug("END CoordinatesController::get_coordinates %s", result)
    return result