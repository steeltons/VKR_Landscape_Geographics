from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, Response, HTTPException
import json
from base_models import Relief
from models.reliefs_model import *
from utils import get_db_connection
router = APIRouter()



@router.get("/reliefs/all", tags=["ReliefController"])
async def reliefs_get_select_all():
    """
      Описание: получение данных обо всех рельефах.
    """
    conn = get_db_connection()
    x = get_reliefs(conn)
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"), status_code=200)

@router.get("/reliefs/one", tags=["ReliefController"])
async def reliefs_get_one_relief(relief_id: int):
    """
      Описание: получение данных об одном рельефе по его ID (кроме картинки).
    """
    conn = get_db_connection()
    x = get_one_relief(conn, relief_id)
    if len(x) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: рельеф с данным ID не найдено.")
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False), status_code=200)

@router.post("/reliefs/delete", tags=["ReliefController"])
async def reliefs_post_delete(relief_id: int):
    """
      Описание: удаление рельефа по его ID.
    """
    conn = get_db_connection()
    y = get_one_relief(conn, relief_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: рельеф с данным ID не найдено, потому удалить его невозможно.")
    x = delete_relief(conn, relief_id)
    return Response("{'messdelete':'Рельеф удалёно.'}", status_code=200)

@router.post("/reliefs/insert", tags=["ReliefController"])
async def reliefs_post_insert(relief_name: str, relief_description: str):
    """
      Описание: добавление рельефа. На ввод подаются название и описание.
      Ограничения: 1) длина названия рельефа должна быть <= 30 символов, и название не должно быть пустым;
                   2) длина описания рельефа должна быть <= 3000 символов, и описание не должно быть пустым;
                   3) название рельефа должно быть уникальным (повторы не допускаются).
    """
    conn = get_db_connection()
    if ((len(relief_name) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: название рельефа не должно быть пустым.")
    if ((len(relief_description) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: описание рельефа не должно быть пустым.")
    if ((len(relief_name) > 30)):
        raise HTTPException(status_code=400, detail="Ошибка: название рельефа должно иметь длину не более 30 символов.")
    if ((len(relief_description) > 3000)):
        raise HTTPException(status_code=400, detail="Ошибка: описание рельефа должно иметь длину не более 3000 символов.")
    y = find_relief_name(conn, relief_name)
    if len(y) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: в базе данных уже есть рельеф с таким названием.")
    x = insert_relief(conn, relief_name, relief_description)
    return Response("{'messinsert':'Рельеф создано.'}", status_code=200)

@router.post("/reliefs/update/name", tags=["ReliefController"])
async def reliefs_post_update_name(relief_id: int, relief_name: str):
    """
      Описание: изменение названия рельефа.
      Ограничения: длина названия рельефа должна быть <= 30 символов, и название не должно быть пустым.
    """
    conn = get_db_connection()
    if ((len(relief_name) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: название рельефа не должно быть пустым.")
    if ((len(relief_name) > 30)):
        raise HTTPException(status_code=400, detail="Ошибка: название рельефа должно иметь длину не более 30 символов.")
    x = update_relief_name(conn, relief_id, relief_name)
    return Response("{'messname':'Название рельефа обновлено.'}", status_code=200)

@router.post("/reliefs/update/description", tags=["ReliefController"])
async def reliefs_post_update_description(relief_id: int, relief_description: str):
    """
      Описание: изменение описания рельефа.
      Ограничения: длина описания рельефа должна быть <= 3000 символов, и описание не должно быть пустым.
    """
    conn = get_db_connection()
    if ((len(relief_description) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: описание рельефа не должно быть пустым.")
    if ((len(relief_description) > 3000)):
        raise HTTPException(status_code=400, detail="Ошибка: описание рельефа должно иметь длину не более 3000 символов.")
    x = update_relief_description(conn, relief_id, relief_description)
    return Response("{'messdescription':'Описание рельефа обновлено.'}", status_code=200)

@router.post("/reliefs/update/picture", tags=["ReliefController"])
async def reliefs_post_update_picture(relief: Relief.ReliefPicture):
    """
      Описание: изменение картинки рельефа.
      Ограничения: длина содержимого файла с картинкой должна быть <= 10000000 символов.
    """
    conn = get_db_connection()
    if ((len(relief.relief_picture) > 10000000)):
        raise HTTPException(status_code=400, detail="Ошибка: содержимое файла с картинкой должно иметь длину не более 10000000 символов.")
    x = update_relief_picture(conn, relief.relief_id, relief.relief_picture)
    return Response("{'messpicture':'Картинка рельефа обновлена.'}", status_code=200)

@router.get("/reliefs/get/picture", tags=["ReliefController"])
async def reliefs_get_picture(relief_id: int):
    """
      Описание: получение картинки рельефа.
    """
    conn = get_db_connection()
    y = get_one_relief(conn, relief_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: рельеф с данным ID не найден, потому получить его картинку невозможно.")
    x = get_relief_picture(conn, relief_id)
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False), status_code=200)
