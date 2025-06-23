from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, Response, HTTPException
import json
from base_models import ConnectionPlantsAnimals
from models.connection_plants_animals_model import *
from models.plants_model import *
from models.animals_model import *
from utils import get_db_connection
router = APIRouter()



@router.get("/connectionplantsanimals/all", tags=["ConnectionController"])
async def connection_plants_animals_get_select_all():
    conn = get_db_connection()
    x = get_connection_plants_animals(conn)
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False), status_code=200)

@router.get("/connectionplantsanimals/one", tags=["ConnectionController"])
async def connection_plants_animals_get_one(connection_plants_animals_id: int):
    conn = get_db_connection()
    y = get_one_connection_plants_animals(conn, connection_plants_animals_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: связь между растением и животным с данным ID не найдена.")
    x = get_one_connection_plants_animals(conn, connection_plants_animals_id)
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False), status_code=200)

@router.post("/connectionplantsanimals/insert", tags=["ConnectionController"])
async def connection_plants_animals_post_insert(plant_id: int, animal_id: int):
    conn = get_db_connection()
    y = get_one_plant(conn, plant_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: растение с данным ID не существует, поэтому его невозможно включить в связь между растением и животным.")
    r = check_one_plants_isFodder(conn, plant_id)
    if len(r) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: растение с данным ID не является кормовым и не может использоваться для кормления скота, поэтому связь между ним и животными создать невозможно.")
    z = get_one_animal(conn, animal_id)
    if len(z) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: животное с данным ID не существует, поэтому его невозможно включить в связь между растением и животным.")
    w = find_connection_plants_animals(conn, plant_id, animal_id)
    if len(w) != 0:
        raise HTTPException(status_code=404, detail="Ошибка: такая связь между растением и животным уже есть.")
    x = insert_connection_plants_animals(conn, plant_id, animal_id)
    return Response("{'messinsert':'Связь между растением и животным (какое животное ест это растение) добавлена.'}", status_code=200)

@router.post("/connectionplantsanimals/delete", tags=["ConnectionController"])
async def connection_plants_animals_post_delete(connection_plants_animals_id: int):
    conn = get_db_connection()
    y = get_one_connection_plants_animals(conn, connection_plants_animals_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: связь между растением и животным с данным ID не найдена, поэтому удалить её невозможно.")
    x = delete_connection_plants_animals(conn, connection_plants_animals_id)
    return Response("{'messdelete':'Связь между растением и животным (какое животное ест это растение) удалена.'}", status_code=200)

@router.post("/connectionplantsanimals/update/plantid", tags=["ConnectionController"])
async def connection_plants_animals_post_update_plant_id(connection_plants_animals_id: int, plant_id: int):
    conn = get_db_connection()
    y = get_one_plant(conn, plant_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: растение с данным ID не существует, поэтому его невозможно включить в связь между растением и животным.")
    r = check_one_plants_isFodder(conn, plant_id)
    if len(r) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: растение с данным ID не является кормовым и не может использоваться для кормления скота, поэтому связь между ним и животными создать невозможно.")
    w = find_connection_plants_animals_plant_id(conn, connection_plants_animals_id, plant_id)
    if len(w) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: такая связь между растением и животным уже есть.")
    x = update_connection_plants_animals_plant_id(conn, connection_plants_animals_id, plant_id)
    return Response("{'messplantid':'ID растения в связи между растением и животным (какое животное ест это растение) обновлён.'}", status_code=200)

@router.post("/connectionplantsanimals/update/animalid", tags=["ConnectionController"])
async def connection_plants_animals_post_update_animal_id(connection_plants_animals_id: int, animal_id: int):
    conn = get_db_connection()
    z = get_one_animal(conn, animal_id)
    if len(z) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: животное с данным ID не существует, поэтому его невозможно включить в связь между растением и животным.")
    w = find_connection_plants_animals_animal_id(conn, connection_plants_animals_id, animal_id)
    if len(w) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: такая связь между растением и животным уже есть.")
    x = update_connection_plants_animals_animal_id(conn, connection_plants_animals_id, animal_id)
    return Response("{'messanimalid':'ID животного в связи между растением и животным (какое животное ест это растение) обновлён.'}", status_code=200)
