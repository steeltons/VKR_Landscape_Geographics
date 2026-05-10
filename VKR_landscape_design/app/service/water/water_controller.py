from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.components.water.water_component import WaterComponent
from app.configs.db.dependencies import get_db
from app.service.water.water_dto import (WaterCreateParamsRqDto, WaterRsDto, WaterUpdateParamsRqDto, WatersRsDto)
from app.service.water.water_dto_mapper import WaterDtoMapper

router = APIRouter(prefix="/api/v1/waters", tags=["waters"])


@router.get("", response_model=WatersRsDto)
def get_waters(
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> WatersRsDto:
    component = WaterComponent(db)
    items = component.get_all(limit=limit, offset=offset)
    return WaterDtoMapper.to_list_rs_dto(items, limit=limit, offset=offset)


@router.get("/{water_id}", response_model=WaterRsDto)
def get_water_by_id(
    water_id: int,
    db: Session = Depends(get_db),
) -> WaterRsDto:
    component = WaterComponent(db)
    item = component.get_by_id(water_id)

    if item is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Water not found")

    return WaterDtoMapper.to_rs_dto(item)


@router.post("", response_model=WaterRsDto, status_code=status.HTTP_201_CREATED)
def create_water(
    request: WaterCreateParamsRqDto,
    db: Session = Depends(get_db),
) -> WaterRsDto:
    component = WaterComponent(db)
    item = component.create(**request.model_dump())
    return WaterDtoMapper.to_rs_dto(item)


@router.patch("/{water_id}", response_model=WaterRsDto)
def update_water(
    water_id: int,
    request: WaterUpdateParamsRqDto,
    db: Session = Depends(get_db),
) -> WaterRsDto:
    component = WaterComponent(db)
    item = component.update(
        water_id=water_id,
        **request.model_dump(exclude_none=True),
    )

    if item is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Water not found")

    return WaterDtoMapper.to_rs_dto(item)


@router.delete("/{water_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_water(
    water_id: int,
    db: Session = Depends(get_db),
) -> None:
    component = WaterComponent(db)

    if not component.deactivate(water_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Water not found")