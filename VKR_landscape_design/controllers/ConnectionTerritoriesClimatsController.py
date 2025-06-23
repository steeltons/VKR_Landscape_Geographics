from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, Response, HTTPException
import json
from base_models import ConnectionTerritoriesClimats
from models.connection_territories_climats_model import *
from models.territories_model import *
from models.climats_model import *
from utils import get_db_connection
router = APIRouter()



@router.get("/connectionterritoriesclimats/all", tags=["ConnectionController"])
async def connection_territories_climats_get_select_all():
    conn = get_db_connection()
    x = get_connection_territories_climats(conn)
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False), status_code=200)

@router.get("/connectionterritoriesclimats/one", tags=["ConnectionController"])
async def connection_territories_climats_get_one(connection_territories_climats_id: int):
    conn = get_db_connection()
    y = get_one_connection_territories_climats(conn, connection_territories_climats_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: связь между территорией и климатом с данным ID не найдена.")
    x = get_one_connection_territories_climats(conn, connection_territories_climats_id)
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False), status_code=200)

@router.post("/connectionterritoriesclimats/insert", tags=["ConnectionController"])
async def connection_territories_climats_post_insert(territorie_id: int, climat_id: int):
    conn = get_db_connection()
    y = get_one_territorie(conn, territorie_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: территория с данным ID не существует, поэтому её невозможно включить в связь между территорией и климатом.")
    z = get_one_climat(conn, climat_id)
    if len(z) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: климат с данным ID не существует, поэтому её невозможно включить в связь между территорией и климатом.")
    w = find_connection_territories_climats(conn, territorie_id, climat_id)
    if len(w) != 0:
        raise HTTPException(status_code=404, detail="Ошибка: такая связь между территорией и климатом уже есть.")
    x = insert_connection_territories_climats(conn, territorie_id, climat_id)
    return Response("{'messinsert':'Связь между территорией и климатом (какой климат есть на этой территории) добавлена.'}", status_code=200)

@router.post("/connectionterritoriesclimats/delete", tags=["ConnectionController"])
async def connection_territories_climats_post_delete(connection_territories_climats_id: int):
    conn = get_db_connection()
    y = get_one_connection_territories_climats(conn, connection_territories_climats_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: связь между территорией и климатом с данным ID не найдена, поэтому удалить её невозможно.")
    x = delete_connection_territories_climats(conn, connection_territories_climats_id)
    return Response("{'messdelete':'Связь между территорией и климатом (какой климат есть на этой территории) удалена.'}", status_code=200)

@router.post("/connectionterritoriesclimats/update/territorieid", tags=["ConnectionController"])
async def connection_territories_climats_post_update_territorie_id(connection_territories_climats_id: int, territorie_id: int):
    conn = get_db_connection()
    y = get_one_territorie(conn, territorie_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: территория с данным ID не существует, поэтому его невозможно включить в связь между территорией и климатом.")
    w = find_connection_territories_climats_territorie_id(conn, connection_territories_climats_id, territorie_id)
    if len(w) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: такая связь между территорией и климатом уже есть.")
    x = update_connection_territories_climats_territorie_id(conn, connection_territories_climats_id, territorie_id)
    return Response("{'messterritorieid':'ID территории в связи между территорией и климатом (какой климат есть на этой территории) обновлён.'}", status_code=200)

@router.post("/connectionterritoriesclimats/update/climatid", tags=["ConnectionController"])
async def connection_territories_climats_post_update_climat_id(connection_territories_climats_id: int, climat_id: int):
    conn = get_db_connection()
    z = get_one_climat(conn, climat_id)
    if len(z) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: климат с данным ID не существует, поэтому его невозможно включить в связь между территорией и климатом.")
    w = find_connection_territories_climats_climat_id(conn, connection_territories_climats_id, climat_id)
    if len(w) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: такая связь между территорией и климатом уже есть.")
    x = update_connection_territories_climats_climat_id(conn, connection_territories_climats_id, climat_id)
    return Response("{'messclimatid':'ID климата в связи между территорией и климатом (какой климат есть на этой территории) обновлён.'}", status_code=200)


