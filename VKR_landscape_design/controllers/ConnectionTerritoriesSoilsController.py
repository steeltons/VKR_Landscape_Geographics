from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, Response, HTTPException
import json
from base_models import ConnectionTerritoriesSoils
from models.connection_territories_soils_model import *
from models.territories_model import *
from models.soils_model import *
from utils import get_db_connection
router = APIRouter()



@router.get("/connectionterritoriessoils/all", tags=["ConnectionController"])
async def connection_territories_soils_get_select_all():
    conn = get_db_connection()
    x = get_connection_territories_soils(conn)
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False), status_code=200)

@router.get("/connectionterritoriessoils/one", tags=["ConnectionController"])
async def connection_territories_soils_get_one(connection_territories_soils_id: int):
    conn = get_db_connection()
    y = get_one_connection_territories_soils(conn, connection_territories_soils_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: связь между территорией и почвой с данным ID не найдена.")
    x = get_one_connection_territories_soils(conn, connection_territories_soils_id)
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False), status_code=200)

@router.post("/connectionterritoriessoils/insert", tags=["ConnectionController"])
async def connection_territories_soils_post_insert(territorie_id: int, soil_id: int):
    conn = get_db_connection()
    y = get_one_territorie(conn, territorie_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: территория с данным ID не существует, поэтому её невозможно включить в связь между территорией и почвой.")
    z = get_one_soil(conn, soil_id)
    if len(z) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: почва с данным ID не существует, поэтому её невозможно включить в связь между территорией и почвой.")
    w = find_connection_territories_soils(conn, territorie_id, soil_id)
    if len(w) != 0:
        raise HTTPException(status_code=404, detail="Ошибка: такая связь между территорией и почвой уже есть.")
    x = insert_connection_territories_soils(conn, territorie_id, soil_id)
    return Response("{'messinsert':'Связь между территорией и почвой (какая почва есть на этой территории) добавлена.'}", status_code=200)

@router.post("/connectionterritoriessoils/delete", tags=["ConnectionController"])
async def connection_territories_soils_post_delete(connection_territories_soils_id: int):
    conn = get_db_connection()
    y = get_one_connection_territories_soils(conn, connection_territories_soils_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: связь между территорией и почвой с данным ID не найдена, поэтому удалить её невозможно.")
    x = delete_connection_territories_soils(conn, connection_territories_soils_id)
    return Response("{'messdelete':'Связь между территорией и почвой (какая почва есть на этой территории) удалена.'}", status_code=200)

@router.post("/connectionterritoriessoils/update/territorieid", tags=["ConnectionController"])
async def connection_territories_soils_post_update_territorie_id(connection_territories_soils_id: int, territorie_id: int):
    conn = get_db_connection()
    y = get_one_territorie(conn, territorie_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: территория с данным ID не существует, поэтому его невозможно включить в связь между территорией и почвой.")
    w = find_connection_territories_soils_territorie_id(conn, connection_territories_soils_id, territorie_id)
    if len(w) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: такая связь между территорией и почвой уже есть.")
    x = update_connection_territories_soils_territorie_id(conn, connection_territories_soils_id, territorie_id)
    return Response("{'messterritorieid':'ID территории в связи между территорией и почвой (какая почва есть на этой территории) обновлён.'}", status_code=200)

@router.post("/connectionterritoriessoils/update/soilid", tags=["ConnectionController"])
async def connection_territories_soils_post_update_soil_id(connection_territories_soils_id: int, soil_id: int):
    conn = get_db_connection()
    z = get_one_soil(conn, soil_id)
    if len(z) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: почва с данным ID не существует, поэтому его невозможно включить в связь между территорией и почвой.")
    w = find_connection_territories_soils_soil_id(conn, connection_territories_soils_id, soil_id)
    if len(w) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: такая связь между территорией и почвой уже есть.")
    x = update_connection_territories_soils_soil_id(conn, connection_territories_soils_id, soil_id)
    return Response("{'messsoilid':'ID почвы в связи между территорией и почвой (какая почва есть на этой территории) обновлён.'}", status_code=200)


