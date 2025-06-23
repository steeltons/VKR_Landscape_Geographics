from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, Response, HTTPException
import json
from base_models import Climat
from models.climats_model import *
from utils import get_db_connection
router = APIRouter()



@router.get("/climats/all", tags=["ClimatController"])
async def climats_get_select_all():
    """
      Описание: получение данных обо всех климатах.
    """
    conn = get_db_connection()
    x = get_climats(conn)
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"), status_code=200)

@router.get("/climats/one", tags=["ClimatController"])
async def climats_get_one_climat(climat_id: int):
    """
      Описание: получение данных об одном климате по его ID (кроме картинки).
    """
    conn = get_db_connection()
    x = get_one_climat(conn, climat_id)
    if len(x) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: климат с данным ID не найдено.")
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False), status_code=200)

@router.post("/climats/delete", tags=["ClimatController"])
async def climats_post_delete(climat_id: int):
    """
      Описание: удаление климата по его ID.
    """
    conn = get_db_connection()
    y = get_one_climat(conn, climat_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: климат с данным ID не найдено, потому удалить его невозможно.")
    x = delete_climat(conn, climat_id)
    return Response("{'messdelete':'Климат удалёно.'}", status_code=200)

@router.post("/climats/insert", tags=["ClimatController"])
async def climats_post_insert(climat_name: str, climat_description: str):
    """
      Описание: добавление климата. На ввод подаются название и описание.
      Ограничения: 1) длина названия климата должна быть <= 30 символов, и название не должно быть пустым;
                   2) длина описания климата должна быть <= 3000 символов, и описание не должно быть пустым;
                   3) название климата должно быть уникальным (повторы не допускаются).
    """
    conn = get_db_connection()
    if ((len(climat_name) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: название климата не должно быть пустым.")
    if ((len(climat_description) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: описание климата не должно быть пустым.")
    if ((len(climat_name) > 30)):
        raise HTTPException(status_code=400, detail="Ошибка: название климата должно иметь длину не более 30 символов.")
    if ((len(climat_description) > 3000)):
        raise HTTPException(status_code=400, detail="Ошибка: описание климата должно иметь длину не более 3000 символов.")
    y = find_climat_name(conn, climat_name)
    if len(y) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: в базе данных уже есть климат с таким названием.")
    x = insert_climat(conn, climat_name, climat_description)
    return Response("{'messinsert':'Климат создано.'}", status_code=200)

@router.post("/climats/update/name", tags=["ClimatController"])
async def climats_post_update_name(climat_id: int, climat_name: str):
    """
      Описание: изменение названия климата.
      Ограничения: длина названия климата должна быть <= 30 символов, и название не должно быть пустым.
    """
    conn = get_db_connection()
    if ((len(climat_name) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: название климата не должно быть пустым.")
    if ((len(climat_name) > 30)):
        raise HTTPException(status_code=400, detail="Ошибка: название климата должно иметь длину не более 30 символов.")
    x = update_climat_name(conn, climat_id, climat_name)
    return Response("{'messname':'Название климата обновлено.'}", status_code=200)

@router.post("/climats/update/description", tags=["ClimatController"])
async def climats_post_update_description(climat_id: int, climat_description: str):
    """
      Описание: изменение описания климата.
      Ограничения: длина описания климата должна быть <= 3000 символов, и описание не должно быть пустым.
    """
    conn = get_db_connection()
    if ((len(climat_description) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: описание климата не должно быть пустым.")
    if ((len(climat_description) > 3000)):
        raise HTTPException(status_code=400, detail="Ошибка: описание климата должно иметь длину не более 3000 символов.")
    x = update_climat_description(conn, climat_id, climat_description)
    return Response("{'messdescription':'Описание климата обновлено.'}", status_code=200)
