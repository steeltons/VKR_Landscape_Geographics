import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.components.landscape.landscape_component import LandscapeComponent
from app.configs.db.dependencies import get_db
from app.service.landscape.landscape_dto import LandscapeCreateParamsRqDto, LandscapeRsDto, LandscapeUpdateParamsRqDto
from app.service.landscape.landscape_dto_mapper import LandscapeDtoMapper

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/landscapes", tags=["landscapes"])


@router.get("", response_model= list[LandscapeRsDto])
def get_landscapes(db: Session = Depends(get_db)) -> list[LandscapeRsDto]:
    logger.debug("START LandscapeController::get_landscapes")

    component = LandscapeComponent(db)
    result = LandscapeDtoMapper.to_list_rs_dto(
        component.get_all()
    )

    logger.debug("END LandscapeController::get_landscapes %s", result)
    return result


@router.get("/{landscape_id}", response_model=LandscapeRsDto)
def get_landscape_by_id(
    landscape_id: int,
    db: Session = Depends(get_db),
) -> LandscapeRsDto:
    params = {"landscape_id": landscape_id}
    logger.debug("START LandscapeController::get_landscape_by_id %s", params)

    component = LandscapeComponent(db)
    item = component.get_by_id(landscape_id)

    if item is None:
        logger.debug("END LandscapeController::get_landscape_by_id %s None", params)
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Landscape not found")

    result = LandscapeDtoMapper.to_rs_dto(item)
    logger.debug("END LandscapeController::get_landscape_by_id %s %s", params, result)
    return result


@router.post("", response_model=LandscapeRsDto, status_code=status.HTTP_201_CREATED)
def create_landscape(
    request: LandscapeCreateParamsRqDto,
    db: Session = Depends(get_db),
) -> LandscapeRsDto:
    params = request.model_dump()
    logger.info("START LandscapeController::create_landscape %s", params)

    component = LandscapeComponent(db)
    result = LandscapeDtoMapper.to_rs_dto(component.create(**params))

    logger.info("END LandscapeController::create_landscape %s %s", params, result)
    return result


@router.patch("/{landscape_id}", response_model=LandscapeRsDto)
def update_landscape(
    landscape_id: int,
    request: LandscapeUpdateParamsRqDto,
    db: Session = Depends(get_db),
) -> LandscapeRsDto:
    params = {"landscape_id": landscape_id, **request.model_dump(exclude_none=True)}
    logger.info("START LandscapeController::update_landscape %s", params)

    component = LandscapeComponent(db)
    item = component.update(**params)

    if item is None:
        logger.info("END LandscapeController::update_landscape %s None", params)
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Landscape not found")

    result = LandscapeDtoMapper.to_rs_dto(item)
    logger.info("END LandscapeController::update_landscape %s %s", params, result)
    return result


@router.delete("/{landscape_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_landscape(
    landscape_id: int,
    db: Session = Depends(get_db),
) -> None:
    params = {"landscape_id": landscape_id}
    logger.info("START LandscapeController::delete_landscape %s", params)

    component = LandscapeComponent(db)
    deleted = component.deactivate(landscape_id)

    logger.info("END LandscapeController::delete_landscape %s %s", params, deleted)

    if not deleted:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Landscape not found")