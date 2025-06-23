from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, Response, HTTPException
import json
from base_models import ConnectionTerritoriesWaters
from models.connection_territories_waters_model import *
from models.territories_model import *
from models.waters_model import *
from utils import get_db_connection
router = APIRouter()



@router.get("/connectionterritorieswaters/all", tags=["ConnectionController"])
async def connection_territories_waters_get_select_all():
    conn = get_db_connection()
    x = get_connection_territories_waters(conn)
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False), status_code=200)

@router.get("/connectionterritorieswaters/one", tags=["ConnectionController"])
async def connection_territories_waters_get_one(connection_territories_waters_id: int):
    conn = get_db_connection()
    y = get_one_connection_territories_waters(conn, connection_territories_waters_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: связь между территорией и водами с данным ID не найдена.")
    x = get_one_connection_territories_waters(conn, connection_territories_waters_id)
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False), status_code=200)

@router.post("/connectionterritorieswaters/insert", tags=["ConnectionController"])
async def connection_territories_waters_post_insert(territorie_id: int, water_id: int):
    conn = get_db_connection()
    y = get_one_territorie(conn, territorie_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: территория с данным ID не существует, поэтому её невозможно включить в связь между территорией и водами.")
    z = get_one_water(conn, water_id)
    if len(z) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: воды с данным ID не существуют, поэтому их невозможно включить в связь между территорией и водами.")
    w = find_connection_territories_waters(conn, territorie_id, water_id)
    if len(w) != 0:
        raise HTTPException(status_code=404, detail="Ошибка: такая связь между территорией и водами уже есть.")
    x = insert_connection_territories_waters(conn, territorie_id, water_id)
    return Response("{'messinsert':'Связь между территорией и водами (какие воды есть на этой территории) добавлена.'}", status_code=200)

@router.post("/connectionterritorieswaters/delete", tags=["ConnectionController"])
async def connection_territories_waters_post_delete(connection_territories_waters_id: int):
    conn = get_db_connection()
    y = get_one_connection_territories_waters(conn, connection_territories_waters_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: связь между территорией и водами с данным ID не найдена, поэтому удалить её невозможно.")
    x = delete_connection_territories_waters(conn, connection_territories_waters_id)
    return Response("{'messdelete':'Связь между территорией и водами (какие воды есть на этой территории) удалена.'}", status_code=200)

@router.post("/connectionterritorieswaters/update/territorieid", tags=["ConnectionController"])
async def connection_territories_waters_post_update_territorie_id(connection_territories_waters_id: int, territorie_id: int):
    conn = get_db_connection()
    y = get_one_territorie(conn, territorie_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: территория с данным ID не существует, поэтому его невозможно включить в связь между территорией и водами.")
    w = find_connection_territories_waters_territorie_id(conn, connection_territories_waters_id, territorie_id)
    if len(w) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: такая связь между территорией и водами уже есть.")
    x = update_connection_territories_waters_territorie_id(conn, connection_territories_waters_id, territorie_id)
    return Response("{'messterritorieid':'ID территории в связи между территорией и водами (какие воды есть на этой территории) обновлён.'}", status_code=200)

@router.post("/connectionterritorieswaters/update/waterid", tags=["ConnectionController"])
async def connection_territories_waters_post_update_water_id(connection_territories_waters_id: int, water_id: int):
    conn = get_db_connection()
    z = get_one_water(conn, water_id)
    if len(z) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: воды с данным ID не существуют, поэтому их невозможно включить в связь между территорией и водами.")
    w = find_connection_territories_waters_water_id(conn, connection_territories_waters_id, water_id)
    if len(w) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: такая связь между территорией и водами уже есть.")
    x = update_connection_territories_waters_water_id(conn, connection_territories_waters_id, water_id)
    return Response("{'messwaterid':'ID вод в связи между территорией и водами (какие воды есть на этой территории) обновлён.'}", status_code=200)



