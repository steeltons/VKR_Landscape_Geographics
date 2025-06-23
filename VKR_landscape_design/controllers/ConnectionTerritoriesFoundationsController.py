from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, Response, HTTPException
import json
from base_models import ConnectionTerritoriesFoundations
from models.connection_territories_foundations_model import *
from models.territories_model import *
from models.foundations_model import *
from utils import get_db_connection
router = APIRouter()



@router.get("/connectionterritoriesfoundations/all", tags=["ConnectionController"])
async def connection_territories_foundations_get_select_all():
    conn = get_db_connection()
    x = get_connection_territories_foundations(conn)
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False), status_code=200)

@router.get("/connectionterritoriesfoundations/one", tags=["ConnectionController"])
async def connection_territories_foundations_get_one(connection_territories_foundations_id: int):
    conn = get_db_connection()
    y = get_one_connection_territories_foundations(conn, connection_territories_foundations_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: связь между территорией и фундаментом с данным ID не найдена.")
    x = get_one_connection_territories_foundations(conn, connection_territories_foundations_id)
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False), status_code=200)

@router.post("/connectionterritoriesfoundations/insert", tags=["ConnectionController"])
async def connection_territories_foundations_post_insert(territorie_id: int, foundation_id: int):
    conn = get_db_connection()
    y = get_one_territorie(conn, territorie_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: территория с данным ID не существует, поэтому её невозможно включить в связь между территорией и фундаментом.")
    z = get_one_foundation(conn, foundation_id)
    if len(z) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: фундамент с данным ID не существует, поэтому её невозможно включить в связь между территорией и фундаментом.")
    w = find_connection_territories_foundations(conn, territorie_id, foundation_id)
    if len(w) != 0:
        raise HTTPException(status_code=404, detail="Ошибка: такая связь между территорией и фундаментом уже есть.")
    x = insert_connection_territories_foundations(conn, territorie_id, foundation_id)
    return Response("{'messinsert':'Связь между территорией и фундаментом (какой фундамент есть на этой территории) добавлена.'}", status_code=200)

@router.post("/connectionterritoriesfoundations/delete", tags=["ConnectionController"])
async def connection_territories_foundations_post_delete(connection_territories_foundations_id: int):
    conn = get_db_connection()
    y = get_one_connection_territories_foundations(conn, connection_territories_foundations_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: связь между территорией и фундаментом с данным ID не найдена, поэтому удалить её невозможно.")
    x = delete_connection_territories_foundations(conn, connection_territories_foundations_id)
    return Response("{'messdelete':'Связь между территорией и фундаментом (какой фундамент есть на этой территории) удалена.'}", status_code=200)

@router.post("/connectionterritoriesfoundations/update/territorieid", tags=["ConnectionController"])
async def connection_territories_foundations_post_update_territorie_id(connection_territories_foundations_id: int, territorie_id: int):
    conn = get_db_connection()
    y = get_one_territorie(conn, territorie_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: территория с данным ID не существует, поэтому его невозможно включить в связь между территорией и фундаментом.")
    w = find_connection_territories_foundations_territorie_id(conn, connection_territories_foundations_id, territorie_id)
    if len(w) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: такая связь между территорией и фундаментом уже есть.")
    x = update_connection_territories_foundations_territorie_id(conn, connection_territories_foundations_id, territorie_id)
    return Response("{'messterritorieid':'ID территории в связи между территорией и фундаментом (какой фундамент есть на этой территории) обновлён.'}", status_code=200)

@router.post("/connectionterritoriesfoundations/update/foundationid", tags=["ConnectionController"])
async def connection_territories_foundations_post_update_foundation_id(connection_territories_foundations_id: int, foundation_id: int):
    conn = get_db_connection()
    z = get_one_foundation(conn, foundation_id)
    if len(z) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: фундамент с данным ID не существует, поэтому его невозможно включить в связь между территорией и фундаментом.")
    w = find_connection_territories_foundations_foundation_id(conn, connection_territories_foundations_id, foundation_id)
    if len(w) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: такая связь между территорией и фундаментом уже есть.")
    x = update_connection_territories_foundations_foundation_id(conn, connection_territories_foundations_id, foundation_id)
    return Response("{'messfoundationid':'ID фундамента в связи между территорией и фундаментом (какой фундамент есть на этой территории) обновлён.'}", status_code=200)
