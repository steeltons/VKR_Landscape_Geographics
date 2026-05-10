import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.components.territory.territory_component import TerritoryComponent
from app.configs.db.dependencies import get_db
from app.service.territory.territory_dto import (TerritoriesRsDto, TerritoryCreateParamsRqDto, TerritoryRsDto,
                                                 TerritoryUpdateParamsRqDto, TerritoryPointSearchRsDto)
from app.service.territory.territory_dto_mapper import TerritoryDtoMapper
from app.service.territory.territory_service import TerritoryService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/territories", tags=["territories"])


@router.get("", response_model=TerritoriesRsDto)
def get_territories(
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> TerritoriesRsDto:
    params = {"limit": limit, "offset": offset}
    logger.debug("START TerritoryController::get_territories %s", params)

    component = TerritoryComponent(db)
    result = TerritoryDtoMapper.to_list_rs_dto(
        component.get_all(limit=limit, offset=offset),
        limit=limit,
        offset=offset,
    )

    logger.debug("END TerritoryController::get_territories %s %s", params, result)
    return result


@router.get("/{territory_id}", response_model=TerritoryRsDto)
def get_territory_by_id(
    territory_id: int,
    db: Session = Depends(get_db),
) -> TerritoryRsDto:
    params = {"territory_id": territory_id}
    logger.debug("START TerritoryController::get_territory_by_id %s", params)

    component = TerritoryComponent(db)
    item = component.get_by_id(territory_id)

    if item is None:
        logger.debug("END TerritoryController::get_territory_by_id %s None", params)
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Territory not found")

    result = TerritoryDtoMapper.to_rs_dto(item)
    logger.debug("END TerritoryController::get_territory_by_id %s %s", params, result)
    return result

@router.get("/by-point/related-objects", response_model=TerritoryPointSearchRsDto)
def get_by_related_points(point_x = Query(...), point_y = Query(...), db: Session = Depends(get_db)):
    params = {"point_x": point_x, "point_y": point_y}
    logger.debug("START TerritoryController::get_by_related_points %s", params)

    service = TerritoryService(db)
    result = service.get_territory_by_point(point_x, point_y)

    if result is None:
        logger.debug(
            "END TerritoryController::get_by_related_points %s None",
            params,
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Точка не принадлежит ни одной территории.",
        )

    logger.debug("END TerritoryController::get_by_related_points %s, %s", params, result)
    return result


@router.post("", response_model=TerritoryRsDto, status_code=status.HTTP_201_CREATED)
def create_territory(
    request: TerritoryCreateParamsRqDto,
    db: Session = Depends(get_db),
) -> TerritoryRsDto:
    params = request.model_dump()
    logger.info("START TerritoryController::create_territory %s", params)

    component = TerritoryComponent(db)
    result = TerritoryDtoMapper.to_rs_dto(component.create(**params))

    logger.info("END TerritoryController::create_territory %s %s", params, result)
    return result


@router.patch("/{territory_id}", response_model=TerritoryRsDto)
def update_territory(
    territory_id: int,
    request: TerritoryUpdateParamsRqDto,
    db: Session = Depends(get_db),
) -> TerritoryRsDto:
    params = {"territory_id": territory_id, **request.model_dump(exclude_none=True)}
    logger.info("START TerritoryController::update_territory %s", params)

    component = TerritoryComponent(db)
    item = component.update(**params)

    if item is None:
        logger.info("END TerritoryController::update_territory %s None", params)
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Territory not found")

    result = TerritoryDtoMapper.to_rs_dto(item)
    logger.info("END TerritoryController::update_territory %s %s", params, result)
    return result


@router.delete("/{territory_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_territory(
    territory_id: int,
    db: Session = Depends(get_db),
) -> None:
    params = {"territory_id": territory_id}
    logger.info("START TerritoryController::delete_territory %s", params)

    component = TerritoryComponent(db)
    deleted = component.deactivate(territory_id)

    logger.info("END TerritoryController::delete_territory %s %s", params, deleted)

    if not deleted:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Territory not found")