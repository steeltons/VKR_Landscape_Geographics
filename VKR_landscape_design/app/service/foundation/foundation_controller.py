from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.components.foundation.foundation_component import FoundationComponent
from app.configs.db.dependencies import get_db
from app.service.foundation.foundation_dto import FoundationCreateParamsRqDto, FoundationRsDto, FoundationUpdateParamsRqDto
from app.service.foundation.foundation_dto_mapper import FoundationDtoMapper

router = APIRouter(prefix="/api/v1/foundations", tags=["foundations"])


@router.get("", response_model= list[FoundationRsDto])
def get_foundations(db: Session = Depends(get_db)) -> list[FoundationRsDto]:
    component = FoundationComponent(db)
    items = component.get_all()
    return FoundationDtoMapper.to_list_rs_dto(items)


@router.get("/{foundation_id}", response_model=FoundationRsDto)
def get_foundation_by_id(
    foundation_id: int,
    db: Session = Depends(get_db),
) -> FoundationRsDto:
    component = FoundationComponent(db)
    item = component.get_by_id(foundation_id)

    if item is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Foundation not found")

    return FoundationDtoMapper.to_rs_dto(item)


@router.post("", response_model=FoundationRsDto, status_code=status.HTTP_201_CREATED)
def create_foundation(
    request: FoundationCreateParamsRqDto,
    db: Session = Depends(get_db),
) -> FoundationRsDto:
    component = FoundationComponent(db)
    item = component.create(**request.model_dump())
    return FoundationDtoMapper.to_rs_dto(item)


@router.patch("/{foundation_id}", response_model=FoundationRsDto)
def update_foundation(
    foundation_id: int,
    request: FoundationUpdateParamsRqDto,
    db: Session = Depends(get_db),
) -> FoundationRsDto:
    component = FoundationComponent(db)
    item = component.update(
        foundation_id=foundation_id,
        **request.model_dump(exclude_none=True),
    )

    if item is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Foundation not found")

    return FoundationDtoMapper.to_rs_dto(item)


@router.delete("/{foundation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_foundation(
    foundation_id: int,
    db: Session = Depends(get_db),
) -> None:
    component = FoundationComponent(db)

    if not component.deactivate(foundation_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Foundation not found")