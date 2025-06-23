from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, Response, HTTPException
import json
from base_models import Landscape
from models.landscapes_model import *
from utils import get_db_connection
router = APIRouter()



@router.get("/landscapes/all", tags=["LandscapeController"])
async def landscapes_get_select_all():
    """
      Описание: получение данных обо всех ландшафтах.
    """
    conn = get_db_connection()
    x = get_landscapes(conn)
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"), status_code=200)

@router.get("/landscapes/one", tags=["LandscapeController"])
async def landscapes_get_one_landscape(landscape_id: int):
    """
      Описание: получение данных об одном ландшафте по его ID (кроме картинки).
    """
    conn = get_db_connection()
    x = get_one_landscape(conn, landscape_id)
    if len(x) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: ландшафт с данным ID не найдено.")
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False), status_code=200)

@router.post("/landscapes/delete", tags=["LandscapeController"])
async def landscapes_post_delete(landscape_id: int):
    """
      Описание: удаление ландшафта по его ID.
    """
    conn = get_db_connection()
    y = get_one_landscape(conn, landscape_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: ландшафт с данным ID не найдено, потому удалить его невозможно.")
    x = delete_landscape(conn, landscape_id)
    return Response("{'messdelete':'Ландшафт удалёно.'}", status_code=200)

@router.post("/landscapes/insert", tags=["LandscapeController"])
async def landscapes_post_insert(landscape_name: str, landscape_description: str):
    """
      Описание: добавление ландшафта. На ввод подаются название и описание.
      Ограничения: 1) длина названия ландшафта должна быть <= 30 символов, и название не должно быть пустым;
                   2) длина описания ландшафта должна быть <= 3000 символов, и описание не должно быть пустым;
                   3) название ландшафта должно быть уникальным (повторы не допускаются).
    """
    conn = get_db_connection()
    if ((len(landscape_name) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: название ландшафта не должно быть пустым.")
    if ((len(landscape_description) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: описание ландшафта не должно быть пустым.")
    if ((len(landscape_name) > 30)):
        raise HTTPException(status_code=400, detail="Ошибка: название ландшафта должно иметь длину не более 30 символов.")
    if ((len(landscape_description) > 3000)):
        raise HTTPException(status_code=400, detail="Ошибка: описание ландшафта должно иметь длину не более 3000 символов.")
    y = find_landscape_name(conn, landscape_name)
    if len(y) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: в базе данных уже есть ландшафт с таким названием.")
    x = insert_landscape(conn, landscape_name, landscape_description)
    return Response("{'messinsert':'Ландшафт создано.'}", status_code=200)

@router.post("/landscapes/update/name", tags=["LandscapeController"])
async def landscapes_post_update_name(landscape_id: int, landscape_name: str):
    """
      Описание: изменение названия ландшафта.
      Ограничения: длина названия ландшафта должна быть <= 30 символов, и название не должно быть пустым.
    """
    conn = get_db_connection()
    if ((len(landscape_name) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: название ландшафта не должно быть пустым.")
    if ((len(landscape_name) > 30)):
        raise HTTPException(status_code=400, detail="Ошибка: название ландшафта должно иметь длину не более 30 символов.")
    x = update_landscape_name(conn, landscape_id, landscape_name)
    return Response("{'messname':'Название ландшафта обновлено.'}", status_code=200)

@router.post("/landscapes/update/description", tags=["LandscapeController"])
async def landscapes_post_update_description(landscape_id: int, landscape_description: str):
    """
      Описание: изменение описания ландшафта.
      Ограничения: длина описания ландшафта должна быть <= 3000 символов, и описание не должно быть пустым.
    """
    conn = get_db_connection()
    if ((len(landscape_description) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: описание ландшафта не должно быть пустым.")
    if ((len(landscape_description) > 3000)):
        raise HTTPException(status_code=400, detail="Ошибка: описание ландшафта должно иметь длину не более 3000 символов.")
    x = update_landscape_description(conn, landscape_id, landscape_description)
    return Response("{'messdescription':'Описание ландшафта обновлено.'}", status_code=200)

@router.post("/landscapes/update/picture", tags=["LandscapeController"])
async def landscapes_post_update_picture(landscape: Landscape.LandscapePicture):
    """
      Описание: изменение картинки ландшафта.
      Ограничения: длина содержимого файла с картинкой должна быть <= 10000000 символов.
    """
    conn = get_db_connection()
    if ((len(landscape.landscape_picture) > 10000000)):
        raise HTTPException(status_code=400, detail="Ошибка: содержимое файла с картинкой должно иметь длину не более 10000000 символов.")
    x = update_landscape_picture(conn, landscape.landscape_id, landscape.landscape_picture)
    return Response("{'messpicture':'Картинка ландшафта обновлена.'}", status_code=200)

@router.get("/landscapes/get/picture", tags=["LandscapeController"])
async def landscapes_get_picture(landscape_id: int):
    """
      Описание: получение картинки ландшафта.
    """
    conn = get_db_connection()
    y = get_one_landscape(conn, landscape_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: ландшафт с данным ID не найден, потому получить его картинку невозможно.")
    x = get_landscape_picture(conn, landscape_id)
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False), status_code=200)
