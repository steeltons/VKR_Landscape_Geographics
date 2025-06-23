from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, Response, HTTPException
import json
from base_models import ConnectionTerritoriesReliefs
from models.connection_territories_reliefs_model import *
from models.territories_model import *
from models.reliefs_model import *
from utils import get_db_connection
router = APIRouter()



@router.get("/connectionterritoriesreliefs/all", tags=["ConnectionController"])
async def connection_territories_reliefs_get_select_all():
    conn = get_db_connection()
    x = get_connection_territories_reliefs(conn)
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False), status_code=200)

@router.get("/connectionterritoriesreliefs/one", tags=["ConnectionController"])
async def connection_territories_reliefs_get_one(connection_territories_reliefs_id: int):
    conn = get_db_connection()
    y = get_one_connection_territories_reliefs(conn, connection_territories_reliefs_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: связь между территорией и рельефом с данным ID не найдена.")
    x = get_one_connection_territories_reliefs(conn, connection_territories_reliefs_id)
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False), status_code=200)

@router.post("/connectionterritoriesreliefs/insert", tags=["ConnectionController"])
async def connection_territories_reliefs_post_insert(territorie_id: int, relief_id: int):
    conn = get_db_connection()
    y = get_one_territorie(conn, territorie_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: территория с данным ID не существует, поэтому её невозможно включить в связь между территорией и рельефом.")
    z = get_one_relief(conn, relief_id)
    if len(z) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: рельеф с данным ID не существует, поэтому её невозможно включить в связь между территорией и рельефом.")
    w = find_connection_territories_reliefs(conn, territorie_id, relief_id)
    if len(w) != 0:
        raise HTTPException(status_code=404, detail="Ошибка: такая связь между территорией и рельефом уже есть.")
    x = insert_connection_territories_reliefs(conn, territorie_id, relief_id)
    return Response("{'messinsert':'Связь между территорией и рельефом (какой рельеф есть на этой территории) добавлена.'}", status_code=200)

@router.post("/connectionterritoriesreliefs/delete", tags=["ConnectionController"])
async def connection_territories_reliefs_post_delete(connection_territories_reliefs_id: int):
    conn = get_db_connection()
    y = get_one_connection_territories_reliefs(conn, connection_territories_reliefs_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: связь между территорией и рельефом с данным ID не найдена, поэтому удалить её невозможно.")
    x = delete_connection_territories_reliefs(conn, connection_territories_reliefs_id)
    return Response("{'messdelete':'Связь между территорией и рельефом (какой рельеф есть на этой территории) удалена.'}", status_code=200)

@router.post("/connectionterritoriesreliefs/update/territorieid", tags=["ConnectionController"])
async def connection_territories_reliefs_post_update_territorie_id(connection_territories_reliefs_id: int, territorie_id: int):
    conn = get_db_connection()
    y = get_one_territorie(conn, territorie_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: территория с данным ID не существует, поэтому его невозможно включить в связь между территорией и рельефом.")
    w = find_connection_territories_reliefs_territorie_id(conn, connection_territories_reliefs_id, territorie_id)
    if len(w) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: такая связь между территорией и рельефом уже есть.")
    x = update_connection_territories_reliefs_territorie_id(conn, connection_territories_reliefs_id, territorie_id)
    return Response("{'messterritorieid':'ID территории в связи между территорией и рельефом (какой рельеф есть на этой территории) обновлён.'}", status_code=200)

@router.post("/connectionterritoriesreliefs/update/reliefid", tags=["ConnectionController"])
async def connection_territories_reliefs_post_update_relief_id(connection_territories_reliefs_id: int, relief_id: int):
    conn = get_db_connection()
    z = get_one_relief(conn, relief_id)
    if len(z) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: рельеф с данным ID не существует, поэтому его невозможно включить в связь между территорией и рельефом.")
    w = find_connection_territories_reliefs_relief_id(conn, connection_territories_reliefs_id, relief_id)
    if len(w) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: такая связь между территорией и рельефом уже есть.")
    x = update_connection_territories_reliefs_relief_id(conn, connection_territories_reliefs_id, relief_id)
    return Response("{'messreliefid':'ID рельефа в связи между территорией и рельефом (какой рельеф есть на этой территории) обновлён.'}", status_code=200)


