from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, Response, HTTPException
import json
from base_models import Water
from models.waters_model import *
from utils import get_db_connection
router = APIRouter()

@router.get("/waters/all", tags=["WaterController"])
async def waters_get_select_all():
    """
      Описание: получение данных обо всех водах.
    """
    conn = get_db_connection()
    x = get_waters(conn)
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"), status_code=200)



@router.get("/waters/one", tags=["WaterController"])
async def waters_get_one_water(water_id: int):
    """
      Описание: получение данных об одних водах по их ID (кроме картинки).
    """
    conn = get_db_connection()
    x = get_one_water(conn, water_id)
    if len(x) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: воды с данным ID не найдены.")
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False), status_code=200)

@router.post("/waters/delete", tags=["WaterController"])
async def waters_post_delete(water_id: int):
    """
      Описание: удаление вод по их ID.
    """
    conn = get_db_connection()
    y = get_one_water(conn, water_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: воды с данным ID не найдены, потому удалить их невозможно.")
    x = delete_water(conn, water_id)
    return Response("{'messdelete':'Ландшафт удалёно.'}", status_code=200)

@router.post("/waters/insert", tags=["WaterController"])
async def waters_post_insert(water_name: str, water_description: str):
    """
      Описание: добавление вод. На ввод подаются название и описание.
      Ограничения: 1) длина названия вод должна быть <= 30 символов, и название не должно быть пустым;
                   2) длина описания вод должна быть <= 3000 символов, и описание не должно быть пустым;
                   3) название вод должно быть уникальным (повторы не допускаются).
    """
    conn = get_db_connection()
    if ((len(water_name) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: название вод не должно быть пустым.")
    if ((len(water_description) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: описание вод не должно быть пустым.")
    if ((len(water_name) > 30)):
        raise HTTPException(status_code=400, detail="Ошибка: название вод должно иметь длину не более 30 символов.")
    if ((len(water_description) > 3000)):
        raise HTTPException(status_code=400, detail="Ошибка: описание вод должно иметь длину не более 3000 символов.")
    y = find_water_name(conn, water_name)
    if len(y) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: в базе данных уже есть воды с таким названием.")
    x = insert_water(conn, water_name, water_description)
    return Response("{'messinsert':'Ландшафт создано.'}", status_code=200)

@router.post("/waters/update/name", tags=["WaterController"])
async def waters_post_update_name(water_id: int, water_name: str):
    """
      Описание: изменение названия вод.
      Ограничения: длина названия вод должна быть <= 30 символов, и название не должно быть пустым.
    """
    conn = get_db_connection()
    if ((len(water_name) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: название вод не должно быть пустым.")
    if ((len(water_name) > 30)):
        raise HTTPException(status_code=400, detail="Ошибка: название вод должно иметь длину не более 30 символов.")
    x = update_water_name(conn, water_id, water_name)
    return Response("{'messname':'Название вод обновлено.'}", status_code=200)

@router.post("/waters/update/description", tags=["WaterController"])
async def waters_post_update_description(water_id: int, water_description: str):
    """
      Описание: изменение описания вод.
      Ограничения: длина описания вод должна быть <= 3000 символов, и описание не должно быть пустым.
    """
    conn = get_db_connection()
    if ((len(water_description) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: описание вод не должно быть пустым.")
    if ((len(water_description) > 3000)):
        raise HTTPException(status_code=400, detail="Ошибка: описание вод должно иметь длину не более 3000 символов.")
    x = update_water_description(conn, water_id, water_description)
    return Response("{'messdescription':'Описание вод обновлено.'}", status_code=200)
