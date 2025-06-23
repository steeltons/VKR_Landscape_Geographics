from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, Response, HTTPException
import json
from base_models import Ground
from models.grounds_model import *
from utils import get_db_connection
router = APIRouter()



@router.get("/grounds/all", tags=["GroundController"])
async def grounds_get_select_all():
    """
      Описание: получение данных обо всех грунтах.
    """
    conn = get_db_connection()
    x = get_grounds(conn)
    return Response((json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace(": NaN", ": null")).replace(".0,", ","), status_code=200)

@router.get("/grounds/one", tags=["GroundController"])
async def grounds_get_one_ground(ground_id: int):
    """
      Описание: получение данных об одном грунте по его ID (кроме картинки).
    """
    conn = get_db_connection()
    x = get_one_ground(conn, ground_id)
    if len(x) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: грунт с данным ID не найден.")
    return Response((json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace(": NaN", ": null")).replace(".0,", ","), status_code=200)

@router.post("/grounds/delete", tags=["GroundController"])
async def grounds_post_delete(ground_id: int):
    """
      Описание: удаление грунта по его ID.
    """
    conn = get_db_connection()
    y = get_one_ground(conn, ground_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: грунт с данным ID не найден, потому удалить его невозможно.")
    x = delete_ground(conn, ground_id)
    return Response("{'messdelete':'Грунт удалён.'}", status_code=200)

@router.post("/grounds/insert", tags=["GroundController"])
async def grounds_post_insert(ground_name: str, ground_description: str):
    """
      Описание: добавление грунта. На ввод подаются название и описание.
      Ограничения: 1) длина названия грунта должна быть <= 30 символов, и название не должно быть пустым;
                   2) длина описания грунта должна быть <= 3000 символов, и описание не должно быть пустым;
                   3) название грунта должно быть уникальным (повторы не допускаются).
    """
    conn = get_db_connection()
    if ((len(ground_name) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: название грунта не должно быть пустым.")
    if ((len(ground_description) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: описание грунта не должно быть пустым.")
    if ((len(ground_name) > 30)):
        raise HTTPException(status_code=400, detail="Ошибка: название грунта должно иметь длину не более 30 символов.")
    if ((len(ground_description) > 3000)):
        raise HTTPException(status_code=400, detail="Ошибка: описание грунта должно иметь длину не более 3000 символов.")
    y = find_ground_name(conn, ground_name)
    if len(y) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: в базе данных уже есть грунт с таким названием.")
    x = insert_ground(conn, ground_name, ground_description)
    return Response("{'messinsert':'Грунт создан.'}", status_code=200)

@router.post("/grounds/update/name", tags=["GroundController"])
async def grounds_post_update_name(ground_id: int, ground_name: str):
    """
      Описание: изменение названия грунта.
      Ограничения: длина названия грунта должна быть <= 30 символов, и название не должно быть пустым.
    """
    conn = get_db_connection()
    if ((len(ground_name) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: название почвы не должно быть пустым.")
    if ((len(ground_name) > 30)):
        raise HTTPException(status_code=400, detail="Ошибка: название грунта должно иметь длину не более 30 символов.")
    x = update_ground_name(conn, ground_id, ground_name)
    return Response("{'messname':'Название грунта обновлено.'}", status_code=200)

@router.post("/grounds/update/description", tags=["GroundController"])
async def grounds_post_update_description(ground_id: int, ground_description: str):
    """
      Описание: изменение описания грунта.
      Ограничения: длина описания животного должна быть <= 3000 символов, и описание не должно быть пустым.
    """
    conn = get_db_connection()
    if ((len(ground_description) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: описание почвы не должно быть пустым.")
    if ((len(ground_description) > 3000)):
        raise HTTPException(status_code=400, detail="Ошибка: описание грунта должно иметь длину не более 3000 символов.")
    x = update_ground_description(conn, ground_id, ground_description)
    return Response("{'messdescription':'Описание грунта обновлено.'}", status_code=200)

@router.post("/grounds/update/density", tags=["GroundController"])
async def grounds_post_update_density(ground_id: int, ground_density: float):
    """
      Описание: изменение плотности грунта в г/см^3.
      Ограничения: плотность грунта в г/см^3 должна принадлежать полуинтервалу (0; 23].
    """
    conn = get_db_connection()
    if ((ground_density <= 0) or (ground_density > 23)):
        raise HTTPException(status_code=400, detail="Ошибка: плотность грунта в г/см^3 должна принадлежать полуинтервалу (0; 23].")
    x = update_ground_density(conn, ground_id, ground_density)
    return Response("{'messdensity':'Плотность грунта в г/см^3 обновлена.'}", status_code=200)

@router.post("/grounds/update/humidity", tags=["GroundController"])
async def grounds_post_update_humidity(ground_id: int, ground_humidity: float):
    """
      Описание: изменение относительной влажности грунта (в процентах).
      Ограничения: относительная влажность грунта (в процентах) должна принадлежать отрезку (0; 100).
    """
    conn = get_db_connection()
    if ((ground_humidity <= 0) or (ground_humidity >= 100)):
        raise HTTPException(status_code=400, detail="Ошибка: относительная влажность грунта (в процентах) должна принадлежать отрезку (0; 100).")
    x = update_ground_humidity(conn, ground_id, ground_humidity)
    return Response("{'messhumidity':'Относительная влажность грунта (в процентах) обновлена.'}", status_code=200)

@router.post("/grounds/update/hardness_Moos", tags=["GroundController"])
async def grounds_post_update_hardness_Moos(ground_id: int, ground_hardness_Moos: int):
    """
      Описание: твёрдости грунта по шкале Мооса.
      Ограничения: твёрдость грунта по шкале Мооса должна быть целым числом, принадлежащим интервалу [1; 10].
    """
    conn = get_db_connection()
    if ((ground_hardness_Moos < 1) or (ground_hardness_Moos > 10)):
        raise HTTPException(status_code=400, detail="Ошибка: твёрдость грунта по шкале Мооса должна быть целым числом, принадлежащим интервалу [1; 10].")
    x = update_ground_hardness_Moos(conn, ground_id, ground_hardness_Moos)
    return Response("{'messhardness_Moos':'Твёрдость грунта по шкале Мооса обновлена.'}", status_code=200)

@router.post("/grounds/update/picture", tags=["GroundController"])
async def grounds_post_update_picture(ground: Ground.GroundPicture):
    """
      Описание: изменение картинки грунта.
      Ограничения: длина содержимого файла с картинкой должна быть <= 10000000 символов.
    """
    conn = get_db_connection()
    if ((len(ground.ground_picture) > 10000000)):
        raise HTTPException(status_code=400, detail="Ошибка: содержимое файла с картинкой должно иметь длину не более 10000000 символов.")
    x = update_ground_picture(conn, ground.ground_id, ground.ground_picture)
    return Response("{'messpicture':'Картинка грунта обновлена.'}", status_code=200)

@router.get("/grounds/get/picture", tags=["GroundController"])
async def grounds_get_picture(ground_id: int):
    """
      Описание: получение картинки грунта.
    """
    conn = get_db_connection()
    y = get_one_ground(conn, ground_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: грунт с данным ID не найден, потому получить его картинку невозможно.")
    x = get_ground_picture(conn, ground_id)
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False), status_code=200)

