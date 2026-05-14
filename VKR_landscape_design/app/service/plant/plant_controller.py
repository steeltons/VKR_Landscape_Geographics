from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.components.plant.plant_component import PlantComponent
from app.configs.db.dependencies import get_db
from app.service.plant.plant_dto import PlantCreateParamsRqDto, PlantRsDto, PlantUpdateParamsRqDto
from app.service.plant.plant_dto_mapper import PlantDtoMapper

router = APIRouter(
    prefix="/api/v1/plants",
    tags=["plants"],
)


@router.get("", response_model= list[PlantRsDto])
def get_plants(db: Session = Depends(get_db)) -> list[PlantRsDto]:
    component = PlantComponent(db)
    plants = component.get_all()

    return PlantDtoMapper.to_list_rs_dto(plants)


@router.get("/{plant_id}", response_model=PlantRsDto)
def get_plant_by_id(
    plant_id: int,
    db: Session = Depends(get_db),
) -> PlantRsDto:
    component = PlantComponent(db)
    plant = component.get_by_id(plant_id)

    if plant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plant not found",
        )

    return PlantDtoMapper.to_rs_dto(plant)


@router.post(
    "",
    response_model=PlantRsDto,
    status_code=status.HTTP_201_CREATED,
)
def create_plant(
    request: PlantCreateParamsRqDto,
    db: Session = Depends(get_db),
) -> PlantRsDto:
    component = PlantComponent(db)

    plant = component.create(
        name=request.name,
        description=request.description,
        picture_id=request.picture_id,
    )

    return PlantDtoMapper.to_rs_dto(plant)


@router.patch("/{plant_id}", response_model=PlantRsDto)
def update_plant(
    plant_id: int,
    request: PlantUpdateParamsRqDto,
    db: Session = Depends(get_db),
) -> PlantRsDto:
    component = PlantComponent(db)

    plant = component.update(
        plant_id=plant_id,
        name=request.name,
        description=request.description,
        picture_id=request.picture_id,
    )

    if plant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plant not found",
        )

    return PlantDtoMapper.to_rs_dto(plant)


@router.delete("/{plant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plant(
    plant_id: int,
    db: Session = Depends(get_db),
) -> None:
    component = PlantComponent(db)

    deleted = component.deactivate(plant_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plant not found",
        )