from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, Response, HTTPException
import json
from base_models import ConnectionTerritoriesLandscapes
from models.connection_territories_landscapes_model import *
from models.territories_model import *
from models.landscapes_model import *
from utils import get_db_connection
router = APIRouter()



@router.get("/connectionterritorieslandscapes/all", tags=["ConnectionController"])
async def connection_territories_landscapes_get_select_all():
    conn = get_db_connection()
    x = get_connection_territories_landscapes(conn)
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False), status_code=200)

@router.get("/connectionterritorieslandscapes/one", tags=["ConnectionController"])
async def connection_territories_landscapes_get_one(connection_territories_landscapes_id: int):
    conn = get_db_connection()
    y = get_one_connection_territories_landscapes(conn, connection_territories_landscapes_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: связь между территорией и ландшафтом с данным ID не найдена.")
    x = get_one_connection_territories_landscapes(conn, connection_territories_landscapes_id)
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False), status_code=200)

@router.post("/connectionterritorieslandscapes/insert", tags=["ConnectionController"])
async def connection_territories_landscapes_post_insert(territorie_id: int, landscape_id: int):
    conn = get_db_connection()
    y = get_one_territorie(conn, territorie_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: территория с данным ID не существует, поэтому её невозможно включить в связь между территорией и ландшафтом.")
    z = get_one_landscape(conn, landscape_id)
    if len(z) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: ландшафт с данным ID не существует, поэтому её невозможно включить в связь между территорией и ландшафтом.")
    w = find_connection_territories_landscapes(conn, territorie_id, landscape_id)
    if len(w) != 0:
        raise HTTPException(status_code=404, detail="Ошибка: такая связь между территорией и ландшафтом уже есть.")
    x = insert_connection_territories_landscapes(conn, territorie_id, landscape_id)
    return Response("{'messinsert':'Связь между территорией и ландшафтом (какой ландшафт есть на этой территории) добавлена.'}", status_code=200)

@router.post("/connectionterritorieslandscapes/delete", tags=["ConnectionController"])
async def connection_territories_landscapes_post_delete(connection_territories_landscapes_id: int):
    conn = get_db_connection()
    y = get_one_connection_territories_landscapes(conn, connection_territories_landscapes_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: связь между территорией и ландшафтом с данным ID не найдена, поэтому удалить её невозможно.")
    x = delete_connection_territories_landscapes(conn, connection_territories_landscapes_id)
    return Response("{'messdelete':'Связь между территорией и ландшафтом (какой ландшафт есть на этой территории) удалена.'}", status_code=200)

@router.post("/connectionterritorieslandscapes/update/territorieid", tags=["ConnectionController"])
async def connection_territories_landscapes_post_update_territorie_id(connection_territories_landscapes_id: int, territorie_id: int):
    conn = get_db_connection()
    y = get_one_territorie(conn, territorie_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: территория с данным ID не существует, поэтому его невозможно включить в связь между территорией и ландшафтом.")
    w = find_connection_territories_landscapes_territorie_id(conn, connection_territories_landscapes_id, territorie_id)
    if len(w) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: такая связь между территорией и ландшафтом уже есть.")
    x = update_connection_territories_landscapes_territorie_id(conn, connection_territories_landscapes_id, territorie_id)
    return Response("{'messterritorieid':'ID территории в связи между территорией и ландшафтом (какой ландшафт есть на этой территории) обновлён.'}", status_code=200)

@router.post("/connectionterritorieslandscapes/update/landscapeid", tags=["ConnectionController"])
async def connection_territories_landscapes_post_update_landscape_id(connection_territories_landscapes_id: int, landscape_id: int):
    conn = get_db_connection()
    z = get_one_landscape(conn, landscape_id)
    if len(z) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: ландшафт с данным ID не существует, поэтому его невозможно включить в связь между территорией и ландшафтом.")
    w = find_connection_territories_landscapes_landscape_id(conn, connection_territories_landscapes_id, landscape_id)
    if len(w) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: такая связь между территорией и ландшафтом уже есть.")
    x = update_connection_territories_landscapes_landscape_id(conn, connection_territories_landscapes_id, landscape_id)
    return Response("{'messlandscapeid':'ID ландшафта в связи между территорией и ландшафтом (какой ландшафт есть на этой территории) обновлён.'}", status_code=200)


