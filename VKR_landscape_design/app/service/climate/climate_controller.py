import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.components.climate.climate_component import ClimateComponent
from app.configs.db.dependencies import get_db
from app.service.climate.climate_dto import ClimateCreateParamsRqDto, ClimateRsDto, ClimateUpdateParamsRqDto
from app.service.climate.climate_dto_mapper import ClimateDtoMapper

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/climates", tags=["climates"])


@router.get("", response_model= list[ClimateRsDto])
def get_climates(db: Session = Depends(get_db)) -> list[ClimateRsDto]:
    logger.debug("START ClimateController::get_climates")

    component = ClimateComponent(db)
    result = ClimateDtoMapper.to_list_rs_dto(component.get_all())

    logger.debug("END ClimateController::get_climates %s", result)
    return result


@router.get("/{climate_id}", response_model=ClimateRsDto)
def get_climate_by_id(
    climate_id: int,
    db: Session = Depends(get_db),
) -> ClimateRsDto:
    params = {"climate_id": climate_id}
    logger.debug("START ClimateController::get_climate_by_id %s", params)

    component = ClimateComponent(db)
    item = component.get_by_id(climate_id)

    if item is None:
        logger.debug("END ClimateController::get_climate_by_id %s None", params)
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Climate not found")

    result = ClimateDtoMapper.to_rs_dto(item)
    logger.debug("END ClimateController::get_climate_by_id %s %s", params, result)
    return result


@router.post("", response_model=ClimateRsDto, status_code=status.HTTP_201_CREATED)
def create_climate(
    request: ClimateCreateParamsRqDto,
    db: Session = Depends(get_db),
) -> ClimateRsDto:
    params = request.model_dump()
    logger.info("START ClimateController::create_climate %s", params)

    component = ClimateComponent(db)
    result = ClimateDtoMapper.to_rs_dto(component.create(**params))

    logger.info("END ClimateController::create_climate %s %s", params, result)
    return result


@router.patch("/{climate_id}", response_model=ClimateRsDto)
def update_climate(
    climate_id: int,
    request: ClimateUpdateParamsRqDto,
    db: Session = Depends(get_db),
) -> ClimateRsDto:
    params = {"climate_id": climate_id, **request.model_dump(exclude_none=True)}
    logger.info("START ClimateController::update_climate %s", params)

    component = ClimateComponent(db)
    item = component.update(**params)

    if item is None:
        logger.info("END ClimateController::update_climate %s None", params)
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Climate not found")

    result = ClimateDtoMapper.to_rs_dto(item)
    logger.info("END ClimateController::update_climate %s %s", params, result)
    return result


@router.delete("/{climate_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_climate(
    climate_id: int,
    db: Session = Depends(get_db),
) -> None:
    params = {"climate_id": climate_id}
    logger.info("START ClimateController::delete_climate %s", params)

    component = ClimateComponent(db)
    deleted = component.deactivate(climate_id)

    logger.info("END ClimateController::delete_climate %s %s", params, deleted)

    if not deleted:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Climate not found")