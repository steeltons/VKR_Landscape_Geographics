from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.components.soil.soil_component import SoilComponent
from app.configs.db.dependencies import get_db
from app.service.soil.dto.soil_dto import (SoilCreateParamsRqDto, SoilRsDto, SoilUpdateParamsRqDto, SoilsRsDto)
from app.service.soil.soil_dto_mapper import SoilDtoMapper

router = APIRouter(
    prefix="/api/v1/soils",
    tags=["soils"],
)


@router.get("", response_model=SoilsRsDto)
def get_soils(
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> SoilsRsDto:
    component = SoilComponent(db)

    soils = component.get_all()

    return SoilDtoMapper.to_list_rs_dto(
        soils,
        limit=limit,
        offset=offset,
    )


@router.get("/{soil_id}", response_model=SoilRsDto)
def get_soil_by_id(
    soil_id: int,
    db: Session = Depends(get_db),
) -> SoilRsDto:
    component = SoilComponent(db)

    soil = component.get_by_id(soil_id)
    if soil is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Soil not found",
        )

    return SoilDtoMapper.to_rs_dto(soil)


@router.post(
    "",
    response_model=SoilRsDto,
    status_code=status.HTTP_201_CREATED,
)
def create_soil(
    request: SoilCreateParamsRqDto,
    db: Session = Depends(get_db),
) -> SoilRsDto:
    component = SoilComponent(db)

    soil = component.create(
        name=request.name,
        description=request.description,
        acidity=request.acidity,
        minerals=request.minerals,
        profile=request.profile,
        picture_id=request.picture_id,
    )

    return SoilDtoMapper.to_rs_dto(soil)


@router.patch("/{soil_id}", response_model=SoilRsDto)
def update_soil(
    soil_id: int,
    request: SoilUpdateParamsRqDto,
    db: Session = Depends(get_db),
) -> SoilRsDto:
    component = SoilComponent(db)

    soil = component.update(
        soil_id=soil_id,
        name=request.name,
        description=request.description,
        acidity=request.acidity,
        minerals=request.minerals,
        profile=request.profile,
        picture_id=request.picture_id,
    )

    if soil is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Soil not found",
        )

    return SoilDtoMapper.to_rs_dto(soil)


@router.delete("/{soil_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_soil(
    soil_id: int,
    db: Session = Depends(get_db),
) -> None:
    component = SoilComponent(db)

    deleted = component.deactivate(soil_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Soil not found",
        )