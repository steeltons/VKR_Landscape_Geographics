from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, Response, HTTPException
import json
import simplejson as sj
from base_models import Territorie
from models.territories_model import *
from utils import get_db_connection
import math
router = APIRouter()


@router.get("/territories/all", tags=["TerritorieController"])
async def territories_get_select_all():
    """
      Описание: получение данных обо всех территориях.
    """
    conn = get_db_connection()
    x = get_territories(conn)
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False), status_code=200)

@router.get("/territories/one", tags=["TerritorieController"])
async def territories_get_one_territorie(territorie_id: int):
    """
      Описание: получение данных об одной территории по её ID.
    """
    conn = get_db_connection()
    x = get_one_territorie(conn, territorie_id)
    if len(x) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: территория с данным ID не найдена.")
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False), status_code=200)

@router.get("/territories/bycoord", tags=["TerritorieController"])
async def territories_bycoord(territorie_coord_x: float, territorie_coord_y: float):
    """
      Описание: получение ближайшей точки по указанным координатам.
    """
    conn = get_db_connection()
    conn.create_function('sqrt', 1, math.sqrt)
    x = bycoord(conn, territorie_coord_x, territorie_coord_y)
    if len(x) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: рядом с указанными координатами нет никаких точек, находящихся в базе данных.")
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False), status_code=200)

@router.get("/territories/byterritoriesoils", tags=["TerritorieController"])
async def territories_byterritorie_soils(user_territorie_id: int):
    """
      Описание: получение данных о присутствующих в данной точке почвах. На ввод подаются координата x (широта) и координата y (долгота).
      Выводится ближайшая точка, в которой есть почвы, если она есть, или ошибка в противном случае.
    """
    conn = get_db_connection()
    y = get_one_territorie(conn, user_territorie_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: такой точки нет в базе данных, поэтому получить перечень присутствующих в ней почв невозможно.")
    x = byterritorie_soils(conn, user_territorie_id)
    return Response((json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace(": NaN", ": null")).replace(".0,", ","), status_code=200)

@router.get("/territories/byterritoriesoilsnoused", tags=["TerritorieController"])
async def territories_byterritorie_soils_noused(user_territorie_id: int):
    """
      Описание: получение данных об отсутствующих в данной точке почвах.
    """
    conn = get_db_connection()
    y = get_one_territorie(conn, user_territorie_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: такой точки нет в базе данных, поэтому получить перечень отсутствующих в ней почв невозможно.")
    x = byterritorie_soils_noused(conn, user_territorie_id)
    return Response((json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace(": NaN", ": null")).replace(".0,", ","), status_code=200)

@router.get("/territories/byterritorieground", tags=["TerritorieController"])
async def territories_byterritorie_ground(user_territorie_id: int):
    """
      Описание: получение данных о присутствующих в данной точке грунтах.
    """
    conn = get_db_connection()
    y = get_one_territorie(conn, user_territorie_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: такой точки нет в базе данных, поэтому получить перечень присутствующих в ней грунтов невозможно.")
    x = byterritorie_ground(conn, user_territorie_id)
    return Response((json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace(": NaN", ": null")).replace(".0,", ","), status_code=200)

@router.get("/territories/byterritorieanimal", tags=["TerritorieController"])
async def territories_byterritorie_animal(user_territorie_id: int):
    """
      Описание: получение данных о присутствующих в данной точке животных.
    """
    conn = get_db_connection()
    y = get_one_territorie(conn, user_territorie_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: такой точки нет в базе данных, поэтому получить информацию о присутствующих в ней животных невозможно.")
    x = byterritorie_animal(conn, user_territorie_id)
    return Response((json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace(": NaN", ": null")).replace(".0,", ","), status_code=200)

@router.get("/territories/byterritorieplant", tags=["TerritorieController"])
async def territories_byterritorie_plant(user_territorie_id: int):
    """
      Описание: получение данных о присутствующих в данной точке растениях.
    """
    conn = get_db_connection()
    y = get_one_territorie(conn, user_territorie_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: такой точки нет в базе данных, поэтому получить информацию о присутствующих в ней растениях невозможно.")
    x = byterritorie_plant(conn, user_territorie_id)
    return Response((json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace(": NaN", ": null")).replace(".0,", ","), status_code=200)

@router.get("/territories/byterritoriefoundations", tags=["TerritorieController"])
async def territories_byterritorie_foundations(user_territorie_id: int):
    """
      Описание: получение данных о присутствующих в данной точке фундаментах.
    """
    conn = get_db_connection()
    y = get_one_territorie(conn, user_territorie_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: такой точки нет в базе данных, поэтому получить перечень присутствующих в ней фундаментов невозможно.")
    x = byterritorie_foundations(conn, user_territorie_id)
    return Response((json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace(": NaN", ": null")).replace(".0,", ","), status_code=200)

@router.get("/territories/byterritoriereliefs", tags=["TerritorieController"])
async def territories_byterritorie_reliefs(user_territorie_id: int):
    """
      Описание: получение данных о присутствующих в данной точке рельефах.
    """
    conn = get_db_connection()
    y = get_one_territorie(conn, user_territorie_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: такой точки нет в базе данных, поэтому получить перечень присутствующих в ней рельефов невозможно.")
    x = byterritorie_reliefs(conn, user_territorie_id)
    return Response((json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace(": NaN", ": null")).replace(".0,", ","), status_code=200)

@router.get("/territories/byterritorielandscapes", tags=["TerritorieController"])
async def territories_byterritorie_landscapes(user_territorie_id: int):
    """
      Описание: получение данных о присутствующих в данной точке ландшафтах.
    """
    conn = get_db_connection()
    y = get_one_territorie(conn, user_territorie_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: такой точки нет в базе данных, поэтому получить перечень присутствующих в ней ландшафтов невозможно.")
    x = byterritorie_landscapes(conn, user_territorie_id)
    return Response((json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace(": NaN", ": null")).replace(".0,", ","), status_code=200)

@router.get("/territories/byterritorieclimats", tags=["TerritorieController"])
async def territories_byterritorie_climats(user_territorie_id: int):
    """
      Описание: получение данных о присутствующих в данной точке климатах.
    """
    conn = get_db_connection()
    y = get_one_territorie(conn, user_territorie_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: такой точки нет в базе данных, поэтому получить перечень присутствующих в ней климатов невозможно.")
    x = byterritorie_climats(conn, user_territorie_id)
    return Response((json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace(": NaN", ": null")).replace(".0,", ","), status_code=200)

@router.get("/territories/byterritoriewaters", tags=["TerritorieController"])
async def territories_byterritorie_waters(user_territorie_id: int):
    """
      Описание: получение данных о присутствующих в данной точке водах.
    """
    conn = get_db_connection()
    y = get_one_territorie(conn, user_territorie_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: такой точки нет в базе данных, поэтому получить перечень присутствующих в ней вод невозможно.")
    x = byterritorie_waters(conn, user_territorie_id)
    return Response((json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace(": NaN", ": null")).replace(".0,", ","), status_code=200)

@router.post("/territories/insert", tags=["TerritorieController"])
async def territories_post_insert(territorie_coord_x: float, territorie_coord_y: float, territorie_address: str):
    """
      Описание: добавление территории. На ввод подаются координата x (широта), координата y (долгота) и адрес.
      Ограничения: 1) координата x (широта) точки должна принадлежать интервалу [-90; 90];
                   2) координата y (долгота) точки должна принадлежать полуинтервалу (-180; 180];
                   3) адрес территории должен иметь длину не более 500 символов и не быть пустым.
    """
    conn = get_db_connection()
    if ((len(territorie_address) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: адрес территории не должен быть пустым.")
    if ((territorie_coord_x < -90) or (territorie_coord_x > 90)):
        raise HTTPException(status_code=400, detail="Ошибка: координата x (широта) точки должна принадлежать интервалу [-90; 90].")
    if ((territorie_coord_y <= -180) or (territorie_coord_y > 180)):
        raise HTTPException(status_code=400, detail="Ошибка: координата y (долгота) точки должна принадлежать полуинтервалу (-180; 180].")
    if (len(territorie_address) > 500):
        raise HTTPException(status_code=400, detail="Ошибка: адрес территории должен быть не длинее 500 символов.")
    x = insert_territorie(conn, territorie_coord_x, territorie_coord_y, territorie_address)
    return Response("{'messinsert':'Территория создана.'}", status_code=200)

@router.post("/territories/delete", tags=["TerritorieController"])
async def territories_post_delete(territorie_id: int):
    """
      Описание: удаление территории по её ID.
    """
    conn = get_db_connection()
    y = get_one_territorie(conn, territorie_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: территория с данным ID не найдена, потому удалить его невозможно.")
    x = delete_territorie(conn, territorie_id)
    return Response("{'messdelete':'Территория удалена.'}", status_code=200)

@router.post("/territories/update/coord_x", tags=["TerritorieController"])
async def territories_post_update_coord_x(territorie_id: int, territorie_coord_x: float):
    """
      Описание: изменение координаты x территории.
      Ограничения: координата x (широта) точки должна принадлежать интервалу [-90; 90].
    """
    conn = get_db_connection()
    if ((territorie_coord_x < -90) or (territorie_coord_x > 90)):
        raise HTTPException(status_code=400, detail="Ошибка: координата x (широта) точки должна принадлежать интервалу [-90; 90].")
    x = update_territorie_coord_x(conn, territorie_id, territorie_coord_x)
    return Response("{'messcoordx':'Координата x (широта) территории обновлена.'}", status_code=200)

@router.post("/territories/update/coord_y", tags=["TerritorieController"])
async def territories_post_update_coord_y(territorie_id: int, territorie_coord_y: float):
    """
      Описание: изменение координаты y территории.
      Ограничения: координата y (долгота) точки должна принадлежать полуинтервалу (-180; 180].
    """
    conn = get_db_connection()
    if ((territorie_coord_y <= -180) or (territorie_coord_y > 180)):
        raise HTTPException(status_code=400, detail="Ошибка: координата y (долгота) точки должна принадлежать полуинтервалу (-180; 180].")
    x = update_territorie_coord_y(conn, territorie_id, territorie_coord_y)
    return Response("{'messcoordy':'Координата y (долгота) территории обновлена.'}", status_code=200)


@router.post("/territories/update/address", tags=["TerritorieController"])
async def territories_post_update_address(territorie_id: int, territorie_address: str):
    """
      Описание: изменение адреса территории.
      Ограничения: адрес территории должен иметь длину не более 500 символов и не быть пустым.
    """
    conn = get_db_connection()
    if ((len(territorie_address) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: адрес территории не должен быть пустым.")
    if (len(territorie_address) > 500):
        raise HTTPException(status_code=400, detail="Ошибка: адрес территории должен иметь длину не более 500 символов.")
    x = update_territorie_address(conn, territorie_id, territorie_address)
    return Response("{'messaddress':'Адрес территории обновлён.'}", status_code=200)


