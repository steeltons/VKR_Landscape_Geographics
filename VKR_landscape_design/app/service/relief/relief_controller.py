from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.components.relief.relief_component import ReliefComponent
from app.configs.db.dependencies import get_db
from app.service.relief.relief_dto import ReliefCreateParamsRqDto, ReliefRsDto, ReliefUpdateParamsRqDto
from app.service.relief.relief_dto_mapper import ReliefDtoMapper

router = APIRouter(prefix="/api/v1/reliefs", tags=["reliefs"])


@router.get("", response_model= list[ReliefRsDto])
def get_reliefs(db: Session = Depends(get_db)) -> list[ReliefRsDto]:
    component = ReliefComponent(db)
    items = component.get_all()
    return ReliefDtoMapper.to_list_rs_dto(items)


@router.get("/{relief_id}", response_model=ReliefRsDto)
def get_relief_by_id(relief_id: int, db: Session = Depends(get_db)) -> ReliefRsDto:
    component = ReliefComponent(db)
    item = component.get_by_id(relief_id)

    if item is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Relief not found")

    return ReliefDtoMapper.to_rs_dto(item)


@router.post("", response_model=ReliefRsDto, status_code=status.HTTP_201_CREATED)
def create_relief(
    request: ReliefCreateParamsRqDto,
    db: Session = Depends(get_db),
) -> ReliefRsDto:
    component = ReliefComponent(db)
    item = component.create(**request.model_dump())
    return ReliefDtoMapper.to_rs_dto(item)


@router.patch("/{relief_id}", response_model=ReliefRsDto)
def update_relief(
    relief_id: int,
    request: ReliefUpdateParamsRqDto,
    db: Session = Depends(get_db),
) -> ReliefRsDto:
    component = ReliefComponent(db)
    item = component.update(
        relief_id=relief_id,
        **request.model_dump(exclude_none=True),
    )

    if item is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Relief not found")

    return ReliefDtoMapper.to_rs_dto(item)


@router.delete("/{relief_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_relief(
    relief_id: int,
    db: Session = Depends(get_db),
) -> None:
    component = ReliefComponent(db)

    if not component.deactivate(relief_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Relief not found")