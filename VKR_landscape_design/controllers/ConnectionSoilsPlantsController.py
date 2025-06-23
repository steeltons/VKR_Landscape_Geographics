from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, Response, HTTPException
import json
from base_models import ConnectionSoilsPlants
from models.connection_soils_plants_model import *
from models.soils_model import *
from models.plants_model import *
from utils import get_db_connection
router = APIRouter()



@router.get("/connectionsoilsplants/all", tags=["ConnectionController"])
async def connection_soils_plants_get_select_all():
    conn = get_db_connection()
    x = get_connection_soils_plants(conn)
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False), status_code=200)

@router.get("/connectionsoilsplants/one", tags=["ConnectionController"])
async def connection_soils_plants_get_one(connection_soils_plants_id: int):
    conn = get_db_connection()
    y = get_one_connection_soils_plants(conn, connection_soils_plants_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: связь между почвой и растением с данным ID не найдена.")
    x = get_one_connection_soils_plants(conn, connection_soils_plants_id)
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False), status_code=200)

@router.post("/connectionsoilsplants/insert", tags=["ConnectionController"])
async def connection_soils_plants_post_insert(soil_id: int, plant_id: int):
    conn = get_db_connection()
    y = get_one_soil(conn, soil_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: почва с данным ID не существует, поэтому её невозможно включить в связь между почвой и растением.")
    z = get_one_plant(conn, plant_id)
    if len(z) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: растение с данным ID не существует, поэтому его невозможно включить в связь между почвой и растением.")
    w = find_connection_soils_plants(conn, soil_id, plant_id)
    if len(w) != 0:
        raise HTTPException(status_code=404, detail="Ошибка: такая связь между почвой и растением уже есть.")
    x = insert_connection_soils_plants(conn, soil_id, plant_id)
    return Response("{'messinsert':'Связь между почвой и растением (какое растение растёт на этой почве) добавлена.'}", status_code=200)

@router.post("/connectionsoilsplants/delete", tags=["ConnectionController"])
async def connection_soils_plants_post_delete(connection_soils_plants_id: int):
    conn = get_db_connection()
    y = get_one_connection_soils_plants(conn, connection_soils_plants_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: связь между почвой и растением с данным ID не найдена, поэтому удалить её невозможно.")
    x = delete_connection_soils_plants(conn, connection_soils_plants_id)
    return Response("{'messdelete':'Связь между почвой и растением (какое растение растёт на этой почве) удалена.'}", status_code=200)

@router.post("/connectionsoilsplants/update/soilid", tags=["ConnectionController"])
async def connection_soils_plants_post_update_soil_id(connection_soils_plants_id: int, soil_id: int):
    conn = get_db_connection()
    y = get_one_soil(conn, soil_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: почва с данным ID не существует, поэтому её невозможно включить в связь между почвой и растением.")
    w = find_connection_soils_plants_soil_id(conn, connection_soils_plants_id, soil_id)
    if len(w) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: такая связь между почвой и растением уже есть.")
    x = update_connection_soils_plants_soil_id(conn, connection_soils_plants_id, soil_id)
    return Response("{'messsoilid':'ID почвы в связи между почвой и растением (какое растение растёт на этой почве) обновлён.'}", status_code=200)

@router.post("/connectionsoilsplants/update/plantid", tags=["ConnectionController"])
async def connection_soils_plants_post_update_plant_id(connection_soils_plants_id: int, plant_id: int):
    conn = get_db_connection()
    z = get_one_plant(conn, plant_id)
    if len(z) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: растение с данным ID не существует, поэтому его невозможно включить в связь между почвой и растением.")
    w = find_connection_soils_plants_plant_id(conn, connection_soils_plants_id, plant_id)
    if len(w) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: такая связь между почвой и растением уже есть.")
    x = update_connection_soils_plants_plant_id(conn, connection_soils_plants_id, plant_id)
    return Response("{'messplantid':'ID растения в связи между почвой и растением (какое растение растёт на этой почве) обновлён.'}", status_code=200)
