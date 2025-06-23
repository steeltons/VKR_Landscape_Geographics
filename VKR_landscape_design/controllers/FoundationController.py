from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, Response, HTTPException
import json
from base_models import Foundation
from models.foundations_model import *
from utils import get_db_connection
router = APIRouter()



@router.get("/foundations/all", tags=["FoundationController"])
async def foundations_get_select_all():
    """
      Описание: получение данных обо всех фундаментах.
    """
    conn = get_db_connection()
    x = get_foundations(conn)
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"), status_code=200)

@router.get("/foundations/one", tags=["FoundationController"])
async def foundations_get_one_foundation(foundation_id: int):
    """
      Описание: получение данных об одном фундаменте по его ID (кроме картинки).
    """
    conn = get_db_connection()
    x = get_one_foundation(conn, foundation_id)
    if len(x) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: фундамент с данным ID не найдено.")
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False), status_code=200)

@router.post("/foundations/delete", tags=["FoundationController"])
async def foundations_post_delete(foundation_id: int):
    """
      Описание: удаление фундамента по его ID.
    """
    conn = get_db_connection()
    y = get_one_foundation(conn, foundation_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: фундамент с данным ID не найдено, потому удалить его невозможно.")
    x = delete_foundation(conn, foundation_id)
    return Response("{'messdelete':'Фундамент удалёно.'}", status_code=200)

@router.post("/foundations/insert", tags=["FoundationController"])
async def foundations_post_insert(foundation_name: str, foundation_description: str):
    """
      Описание: добавление фундамента. На ввод подаются название и описание.
      Ограничения: 1) длина названия фундамента должна быть <= 30 символов, и название не должно быть пустым;
                   2) длина описания фундамента должна быть <= 3000 символов, и описание не должно быть пустым;
                   3) название фундамента должно быть уникальным (повторы не допускаются).
    """
    conn = get_db_connection()
    if ((len(foundation_name) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: название фундамента не должно быть пустым.")
    if ((len(foundation_description) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: описание фундамента не должно быть пустым.")
    if ((len(foundation_name) > 30)):
        raise HTTPException(status_code=400, detail="Ошибка: название фундамента должно иметь длину не более 30 символов.")
    if ((len(foundation_description) > 3000)):
        raise HTTPException(status_code=400, detail="Ошибка: описание фундамента должно иметь длину не более 3000 символов.")
    y = find_foundation_name(conn, foundation_name)
    if len(y) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: в базе данных уже есть фундамент с таким названием.")
    x = insert_foundation(conn, foundation_name, foundation_description)
    return Response("{'messinsert':'Фундамент создано.'}", status_code=200)

@router.post("/foundations/update/name", tags=["FoundationController"])
async def foundations_post_update_name(foundation_id: int, foundation_name: str):
    """
      Описание: изменение названия фундамента.
      Ограничения: длина названия фундамента должна быть <= 30 символов, и название не должно быть пустым.
    """
    conn = get_db_connection()
    if ((len(foundation_name) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: название фундамента не должно быть пустым.")
    if ((len(foundation_name) > 30)):
        raise HTTPException(status_code=400, detail="Ошибка: название фундамента должно иметь длину не более 30 символов.")
    x = update_foundation_name(conn, foundation_id, foundation_name)
    return Response("{'messname':'Название фундамента обновлено.'}", status_code=200)

@router.post("/foundations/update/description", tags=["FoundationController"])
async def foundations_post_update_description(foundation_id: int, foundation_description: str):
    """
      Описание: изменение описания фундамента.
      Ограничения: длина описания фундамента должна быть <= 3000 символов, и описание не должно быть пустым.
    """
    conn = get_db_connection()
    if ((len(foundation_description) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: описание фундамента не должно быть пустым.")
    if ((len(foundation_description) > 3000)):
        raise HTTPException(status_code=400, detail="Ошибка: описание фундамента должно иметь длину не более 3000 символов.")
    x = update_foundation_description(conn, foundation_id, foundation_description)
    return Response("{'messdescription':'Описание фундамента обновлено.'}", status_code=200)

@router.post("/foundations/update/picture", tags=["FoundationController"])
async def foundations_post_update_picture(foundation: Foundation.FoundationPicture):
    """
      Описание: изменение картинки фундамента.
      Ограничения: длина содержимого файла с картинкой должна быть <= 10000000 символов.
    """
    conn = get_db_connection()
    if ((len(foundation.foundation_picture) > 10000000)):
        raise HTTPException(status_code=400, detail="Ошибка: содержимое файла с картинкой должно иметь длину не более 10000000 символов.")
    x = update_foundation_picture(conn, foundation.foundation_id, foundation.foundation_picture)
    return Response("{'messpicture':'Картинка фундамента обновлена.'}", status_code=200)

@router.get("/foundations/get/picture", tags=["FoundationController"])
async def foundations_get_picture(foundation_id: int):
    """
      Описание: получение картинки фундамента.
    """
    conn = get_db_connection()
    y = get_one_foundation(conn, foundation_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: фундамент с данным ID не найден, потому получить его картинку невозможно.")
    x = get_foundation_picture(conn, foundation_id)
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False), status_code=200)
