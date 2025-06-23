from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, Response, HTTPException
import json
from base_models import Soil
from models.soils_model import *
from utils import get_db_connection
router = APIRouter()



@router.get("/soils/all", tags=["SoilController"])
async def soils_get_select_all():
    """
      Описание: получение данных обо всех почвах.
    """
    conn = get_db_connection()
    x = get_soils(conn)
    return Response((json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace(": NaN", ": null")).replace(".0,", ","), status_code=200)

@router.get("/soils/one", tags=["SoilController"])
async def soils_get_one_soil(soil_id: int):
    """
      Описание: получение данных об одной почве по её ID (кроме картинки).
    """
    conn = get_db_connection()
    x = get_one_soil(conn, soil_id)
    if len(x) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: почва с данным ID не найдена.")
    return Response((json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace(": NaN", ": null")).replace(".0,", ","), status_code=200)

@router.get("/soils/bysoilgrounds", tags=["SoilController"])
async def soils_bysoil_grounds(soil_id: int):
    """
      Описание: получение списка грунтов, характерных для почвы с заданным ID.
    """
    conn = get_db_connection()
    y = get_one_soil(conn, soil_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: почва с данным ID не найдена, потому получить перечень характерных для неё грунтов невозможно.")
    x = bysoil_grounds(conn, soil_id)
    return Response((json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace(": NaN", ": null")).replace(".0,", ","), status_code=200)

@router.get("/soils/bysoilgroundsnoused", tags=["SoilController"])
async def soils_bysoil_grounds_noused(soil_id: int):
    """
      Описание: получение списка грунтов, нехарактерных для почвы с заданным ID.
    """
    conn = get_db_connection()
    y = get_one_soil(conn, soil_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: почва с данным ID не найдена, потому получить перечень нехарактерных для неё грунтов невозможно.")
    x = bysoil_grounds_noused(conn, soil_id)
    return Response((json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace(": NaN", ": null")).replace(".0,", ","), status_code=200)

@router.get("/soils/bysoilplants", tags=["SoilController"])
async def soils_bysoil_plants(soil_id: int):
    """
      Описание: получение списка растений, подходящих для почвы с заданным ID.
    """
    conn = get_db_connection()
    y = get_one_soil(conn, soil_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: почва с данным ID не найдена, потому получить перечень подходящих для неё растений невозможно.")
    x = bysoil_plants(conn, soil_id)
    return Response((json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace(": NaN", ": null")).replace(".0,", ","), status_code=200)

@router.get("/soils/bysoilplantsnoused", tags=["SoilController"])
async def soils_bysoil_plants_noused(soil_id: int):
    """
      Описание: получение списка растений, неподходящих для почвы с заданным ID.
    """
    conn = get_db_connection()
    y = get_one_soil(conn, soil_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: почва с данным ID не найдена, потому получить перечень нерастущих на ней растений невозможно.")
    x = bysoil_plants_noused(conn, soil_id)
    return Response((json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace(": NaN", ": null")).replace(".0,", ","), status_code=200)

@router.post("/soils/delete", tags=["SoilController"])
async def soils_post_delete(soil_id: int):
    """
      Описание: удаление почвы по её ID.
    """
    conn = get_db_connection()
    y = get_one_soil(conn, soil_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: почва с данным ID не найдена, потому удалить её невозможно.")
    x = delete_soil(conn, soil_id)
    return Response("{'messdelete':'Почва удалена.'}", status_code=200)

@router.post("/soils/insert", tags=["SoilController"])
async def soils_post_insert(soil_name: str, soil_description: str):
    """
      Описание: добавление почвы. На ввод подаются название и описание.
      Ограничения: 1) длина названия почвы должна быть <= 40 символов, и название не должно быть пустым;
                   2) длина описания почвы должна быть <= 3000 символов, и описание не должно быть пустым;
                   3) название почвы должно быть уникальным (повторы не допускаются).
    """
    conn = get_db_connection()
    if ((len(soil_name) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: название почвы не должно быть пустым.")
    if ((len(soil_description) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: описание почвы не должно быть пустым.")
    if ((len(soil_name) > 40)):
        raise HTTPException(status_code=400, detail="Ошибка: название почвы должно иметь длину не более 40 символов.")
    if ((len(soil_description) > 3000)):
        raise HTTPException(status_code=400, detail="Ошибка: описание почвы должно иметь длину не более 3000 символов.")
    y = find_soil_name(conn, soil_name)
    if len(y) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: в базе данных уже есть почва с таким названием.")
    x = insert_soil(conn, soil_name, soil_description)
    return Response("{'messinsert':'Почва создана.'}", status_code=200)

@router.post("/soils/update/name", tags=["SoilController"])
async def soils_post_update_name(soil_id: int, soil_name: str):
    """
      Описание: изменение названия почвы.
      Ограничения: длина названия почвы должна быть <= 40 символов, и название не должно быть пустым.
    """
    conn = get_db_connection()
    if ((len(soil_name) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: название почвы не должно быть пустым.")
    if ((len(soil_name) > 40)):
        raise HTTPException(status_code=400, detail="Ошибка: название почвы должно иметь длину не более 40 символов.")
    x = update_soil_name(conn, soil_id, soil_name)
    return Response("{'messname':'Название почвы обновлено.'}", status_code=200)

@router.post("/soils/update/description", tags=["SoilController"])
async def soils_post_update_description(soil_id: int, soil_description: str):
    """
      Описание: изменение описания грунта.
      Ограничения: длина описания животного должна быть <= 3000 символов, и описание не должно быть пустым.
    """
    conn = get_db_connection()
    if ((len(soil_description) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: описание почвы не должно быть пустым.")
    if ((len(soil_description) > 3000)):
        raise HTTPException(status_code=400, detail="Ошибка: описание почвы должно иметь длину не более 3000 символов.")
    x = update_soil_description(conn, soil_id, soil_description)
    return Response("{'messdescription':'Описание почвы обновлено.'}", status_code=200)

@router.post("/soils/update/acidity", tags=["SoilController"])
async def soils_post_update_acidity(soil_id: int, soil_acidity: float):
    """
      Описание: изменение кислотности почвы в pH.
      Ограничения: кислотность почвы в pH должна принадлежать полуинтервалу (0; 20].
    """
    conn = get_db_connection()
    if ((soil_acidity <= 0) or (soil_acidity > 20)):
        raise HTTPException(status_code=400, detail="Ошибка: кислотность почвы в pH должна принадлежать полуинтервалу (0; 20].")
    x = update_soil_acidity(conn, soil_id, soil_acidity)
    return Response("{'messacidity':'Кислотность почвы в pH обновлена.'}", status_code=200)

@router.post("/soils/update/minerals", tags=["SoilController"])
async def soils_post_update_minerals(soil_id: int, soil_minerals: str):
    """
      Описание: изменение минерального состава почвы.
      Ограничения: минеральный состав почвы должен иметь длину не более 1000 символов.
    """
    conn = get_db_connection()
    if ((len(soil_minerals) > 1000)):
        raise HTTPException(status_code=400, detail="Ошибка: минеральный состав почвы должен иметь длину не более 1000 символов.")
    x = update_soil_minerals(conn, soil_id, soil_minerals)
    return Response("{'messminerals':'Минеральный состав почвы обновлён.'}", status_code=200)

@router.post("/soils/update/profile", tags=["SoilController"])
async def soils_post_update_profile(soil_id: int, soil_profile: str):
    """
      Описание: изменение профиля почвы.
      Ограничения: профиль почвы должен иметь длину не более 250 символов.
    """
    conn = get_db_connection()
    if ((len(soil_profile) < 2) or (len(soil_profile) > 250)):
        raise HTTPException(status_code=400, detail="Ошибка: профиль почвы должен иметь длину не более 250 символов.")
    x = update_soil_profile(conn, soil_id, soil_profile)
    return Response("{'messprofile':'Профиль почвы обновлён.'}", status_code=200)

@router.post("/soils/update/picture", tags=["SoilController"])
async def soils_post_update_picture(soil: Soil.SoilPicture):
    """
      Описание: изменение картинки почвы.
      Ограничения: длина содержимого файла с картинкой должна быть <= 10000000 символов.
    """
    conn = get_db_connection()
    if ((len(soil.soil_picture) > 10000000)):
        raise HTTPException(status_code=400, detail="Ошибка: содержимое файла с картинкой должно иметь длину не более 10000000 символов.")
    x = update_soil_picture(conn, soil.soil_id, soil.soil_picture)
    return Response("{'messpicture':'Картинка почвы обновлена.'}", status_code=200)

@router.get("/soils/get/picture", tags=["SoilController"])
async def soils_get_picture(soil_id: int):
    """
      Описание: получение картинки почвы.
    """
    conn = get_db_connection()
    y = get_one_soil(conn, soil_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: почва с данным ID не найдена, потому получить её картинку невозможно.")
    x = get_soil_picture(conn, soil_id)
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False), status_code=200)