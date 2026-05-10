from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.components.ground.ground_component import GroundComponent
from app.configs.db.dependencies import get_db
from app.service.ground.ground_dto import (GroundCreateParamsRqDto, GroundRsDto, GroundUpdateParamsRqDto, GroundsRsDto)
from app.service.ground.ground_dto_mapper import GroundDtoMapper

router = APIRouter(
    prefix="/api/v1/grounds",
    tags=["grounds"],
)


@router.get("", response_model=GroundsRsDto)
def get_grounds(
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> GroundsRsDto:
    component = GroundComponent(db)
    grounds = component.get_all(limit=limit, offset=offset)

    return GroundDtoMapper.to_list_rs_dto(
        grounds,
        limit=limit,
        offset=offset,
    )


@router.get("/{ground_id}", response_model=GroundRsDto)
def get_ground_by_id(
    ground_id: int,
    db: Session = Depends(get_db),
) -> GroundRsDto:
    component = GroundComponent(db)
    ground = component.get_by_id(ground_id)

    if ground is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ground not found",
        )

    return GroundDtoMapper.to_rs_dto(ground)


@router.post(
    "",
    response_model=GroundRsDto,
    status_code=status.HTTP_201_CREATED,
)
def create_ground(
    request: GroundCreateParamsRqDto,
    db: Session = Depends(get_db),
) -> GroundRsDto:
    component = GroundComponent(db)

    ground = component.create(
        name=request.name,
        description=request.description,
        density=request.density,
        humidity=request.humidity,
        solidity=request.solidity,
        picture_id=request.picture_id,
    )

    return GroundDtoMapper.to_rs_dto(ground)


@router.patch("/{ground_id}", response_model=GroundRsDto)
def update_ground(
    ground_id: int,
    request: GroundUpdateParamsRqDto,
    db: Session = Depends(get_db),
) -> GroundRsDto:
    component = GroundComponent(db)

    ground = component.update(
        ground_id=ground_id,
        name=request.name,
        description=request.description,
        density=request.density,
        humidity=request.humidity,
        solidity=request.solidity,
        picture_id=request.picture_id,
    )

    if ground is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ground not found",
        )

    return GroundDtoMapper.to_rs_dto(ground)


@router.delete("/{ground_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ground(
    ground_id: int,
    db: Session = Depends(get_db),
) -> None:
    component = GroundComponent(db)

    deleted = component.deactivate(ground_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ground not found",
        )