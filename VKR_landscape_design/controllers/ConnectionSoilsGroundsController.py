from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, Response, HTTPException
import json
from base_models import ConnectionSoilsGrounds
from models.connection_soils_grounds_model import *
from models.soils_model import *
from models.grounds_model import *
from utils import get_db_connection
router = APIRouter()



@router.get("/connectionsoilsgrounds/all", tags=["ConnectionController"])
async def connection_soils_grounds_get_select_all():
    conn = get_db_connection()
    x = get_connection_soils_grounds(conn)
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False), status_code=200)

@router.get("/connectionsoilsgrounds/one", tags=["ConnectionController"])
async def connection_soils_grounds_get_one(connection_soils_grounds_id: int):
    conn = get_db_connection()
    y = get_one_connection_soils_grounds(conn, connection_soils_grounds_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: связь между почвой и грунтом с данным ID не найдена.")
    x = get_one_connection_soils_grounds(conn, connection_soils_grounds_id)
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False), status_code=200)

@router.post("/connectionsoilsgrounds/insert", tags=["ConnectionController"])
async def connection_soils_grounds_post_insert(soil_id: int, ground_id: int):
    conn = get_db_connection()
    y = get_one_soil(conn, soil_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: почва с данным ID не существует, поэтому её невозможно включить в связь между почвой и грунтом.")
    z = get_one_ground(conn, ground_id)
    if len(z) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: грунт с данным ID не существует, поэтому её невозможно включить в связь между почвой и грунтом.")
    w = find_connection_soils_grounds(conn, soil_id, ground_id)
    if len(w) != 0:
        raise HTTPException(status_code=404, detail="Ошибка: такая связь между почвой и грунтом уже есть.")
    x = insert_connection_soils_grounds(conn, soil_id, ground_id)
    return Response("{'messinsert':'Связь между почвой и грунтом (какой грунт встречается на этой почве) добавлена.'}", status_code=200)

@router.post("/connectionsoilsgrounds/delete", tags=["ConnectionController"])
async def connection_soils_grounds_post_delete(connection_soils_grounds_id: int):
    conn = get_db_connection()
    y = get_one_connection_soils_grounds(conn, connection_soils_grounds_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: связь между почвой и грунтом с данным ID не найдена, поэтому удалить её невозможно.")
    x = delete_connection_soils_grounds(conn, connection_soils_grounds_id)
    return Response("{'messdelete':'Связь между почвой и грунтом (какой грунт встречается на этой почве) удалена.'}", status_code=200)

@router.post("/connectionsoilsgrounds/update/soilid", tags=["ConnectionController"])
async def connection_soils_grounds_post_update_soil_id(connection_soils_grounds_id: int, soil_id: int):
    conn = get_db_connection()
    y = get_one_soil(conn, soil_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: почва с данным ID не существует, поэтому её невозможно включить в связь между почвой и грунтом.")
    w = find_connection_soils_grounds_soil_id(conn, connection_soils_grounds_id, soil_id)
    if len(w) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: такая связь между почвой и грунтом уже есть.")
    x = update_connection_soils_grounds_soil_id(conn, connection_soils_grounds_id, soil_id)
    return Response("{'messsoilid':'ID почвы в связи между почвой и грунтом (какой грунт встречается на этой почве) обновлён.'}", status_code=200)

@router.post("/connectionsoilsgrounds/update/groundid", tags=["ConnectionController"])
async def connection_soils_grounds_post_update_ground_id(connection_soils_grounds_id: int, ground_id: int):
    conn = get_db_connection()
    z = get_one_ground(conn, ground_id)
    if len(z) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: грунт с данным ID не существует, поэтому его невозможно включить в связь между почвой и грунтом.")
    w = find_connection_soils_grounds_ground_id(conn, connection_soils_grounds_id, ground_id)
    if len(w) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: такая связь между почвой и грунтом уже есть.")
    x = update_connection_soils_grounds_ground_id(conn, connection_soils_grounds_id, ground_id)
    return Response("{'messgroundid':'ID грунта в связи между почвой и грунтом (какой грунт встречается на этой почве) обновлён.'}", status_code=200)



