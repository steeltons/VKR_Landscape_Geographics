from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, Response, HTTPException
import json
from base_models import Plant
from models.plants_model import *
from utils import get_db_connection
router = APIRouter()


@router.get("/plants/all", tags=["PlantController"])
async def plants_get_select_all():
    """
      Описание: получение данных обо всех растениях.
    """
    conn = get_db_connection()
    x = get_plants(conn)
    return Response((json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace(": NaN", ": null")).replace(".0,", ","), status_code=200)

@router.get("/plants/one", tags=["PlantController"])
async def plants_get_one_plant(plant_id: int):
    """
      Описание: получение данных об одном растении по его ID (кроме картинки).
    """
    conn = get_db_connection()
    x = get_one_plant(conn, plant_id)
    if len(x) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: растение с данным ID не найдено.")
    return Response((json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace(": NaN", ": null")).replace(".0,", ","), status_code=200)

@router.get("/plants/allisFodder", tags=["PlantController"])
async def plants_get_select_isFodder():
    """
      Описание: получение данных обо всех кормовых растениях (то есть подходящих для выпаса скота).
    """
    conn = get_db_connection()
    x = get_plants_isFodder(conn)
    return Response((json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace(": NaN", ": null")).replace(".0,", ","), status_code=200)

@router.get("/plants/allisNoFodder", tags=["PlantController"])
async def plants_get_select_isNoFodder():
    """
      Описание: получение данных обо всех некормовых растениях (то есть не подходящих для выпаса скота).
    """
    conn = get_db_connection()
    x = get_plants_isNoFodder(conn)
    return Response((json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace(": NaN", ": null")).replace(".0,", ","), status_code=200)

@router.get("/plants/byplantanimals", tags=["PlantController"])
async def plants_byplant_animals(plant_id: int):
    """
      Описание: получение перечня животных, которые питаются растением с заданным ID.
    """
    conn = get_db_connection()
    y = get_one_plant(conn, plant_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: растение с данным ID не найдено, потому получить перечень животных, которые им питаются, невозможно.")
    x = byplant_animals(conn, plant_id)
    return Response((json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace(": NaN", ": null")).replace(".0,", ","), status_code=200)

@router.get("/plants/byplantanimalsnoused", tags=["PlantController"])
async def plants_byplant_animals_noused(plant_id: int):
    """
      Описание: получение перечня животных, которые не питаются растением с заданным ID.
    """
    conn = get_db_connection()
    y = get_one_plant(conn, plant_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: растение с данным ID не найдено, потому получить перечень животных, которые им не питаются, невозможно.")
    x = byplant_animals_noused(conn, plant_id)
    return Response((json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace(": NaN", ": null")).replace(".0,", ","), status_code=200)

@router.post("/plants/delete", tags=["PlantController"])
async def plants_post_delete(plant_id: int):
    """
      Описание: удаление растения по его ID.
    """
    conn = get_db_connection()
    y = get_one_plant(conn, plant_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: растение с данным ID не найдено, потому удалить его невозможно.")
    x = delete_plant(conn, plant_id)
    return Response("{'messdelete':'Растение удалёно.'}", status_code=200)

@router.post("/plants/insert", tags=["PlantController"])
async def plants_post_insert(plant_name: str, plant_description: str, plant_isFodder: int):
    """
      Описание: добавление растения. На ввод подаются название, описание и то, является ли растение кормовым.
      Ограничения: 1) название растения должно иметь длину не более 50 символов, и название не должно быть пустым;
                   2) описание растения должно иметь длину не более 3000 символов, и описание не должно быть пустым;
                   3) растение может быть только или некормовым (0), или кормовым (1);
                   4) название растения должно быть уникальным (повторы не допускаются).
    """
    conn = get_db_connection()
    if ((len(plant_name) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: название растения не должно быть пустым.")
    if ((len(plant_description) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: описание растения не должно быть пустым.")
    if ((len(plant_name) > 50)):
        raise HTTPException(status_code=400, detail="Ошибка: название растения должно иметь длину не более 50 символов.")
    if ((len(plant_description) > 3000)):
        raise HTTPException(status_code=400, detail="Ошибка: описание растения должно иметь длину не более 3000 символов.")
    if ((plant_isFodder < 0) or (plant_isFodder > 1)):
        raise HTTPException(status_code=400, detail="Ошибка: растение может быть только или некормовым (0), или кормовым (1).")
    y = find_plant_name(conn, plant_name)
    if len(y) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: в базе данных уже есть растение с таким названием.")
    x = insert_plant(conn, plant_name, plant_description, plant_isFodder)
    return Response("{'messinsert':'Растение создано.'}", status_code=200)

@router.post("/plants/update/name", tags=["PlantController"])
async def plants_post_update_name(plant_id: int, plant_name: str):
    """
      Описание: изменение названия растения.
      Ограничения: длина названия растения должна быть <= 50 символов, и название не должно быть пустым.
    """
    conn = get_db_connection()
    if ((len(plant_name) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: название почвы не должно быть пустым.")
    if ((len(plant_name) > 50)):
        raise HTTPException(status_code=400, detail="Ошибка: название растения должно иметь длину не более 50 символов.")
    x = update_plant_name(conn, plant_id, plant_name)
    return Response("{'messname':'Название растения обновлено.'}", status_code=200)

@router.post("/plants/update/description", tags=["PlantController"])
async def plants_post_update_description(plant_id: int, plant_description: str):
    """
      Описание: изменение описания почвы.
      Ограничения: длина описания почвы должна быть <= 3000 символов, и описание не должно быть пустым.
    """
    conn = get_db_connection()
    if ((len(plant_description) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: описание почвы не должно быть пустым.")
    if ((len(plant_description) > 3000)):
        raise HTTPException(status_code=400, detail="Ошибка: описание растения должно иметь длину не более 3000 символов.")
    x = update_plant_description(conn, plant_id, plant_description)
    return Response("{'messdescription':'Описание растения обновлено.'}", status_code=200)

@router.post("/plants/update/isFodder", tags=["PlantController"])
async def plants_post_update_isFodder(plant_id: int, plant_isFodder: int):
    """
      Описание: изменение того, является растение кормовым или нет.
      Ограничения: растение может быть только или некормовым (0), или кормовым (1).
    """
    conn = get_db_connection()
    if ((plant_isFodder < 0) or (plant_isFodder > 1)):
        raise HTTPException(status_code=400, detail="Ошибка: растение может быть только или некормовым (0), или кормовым (1).")
    x = update_plant_isFodder(conn, plant_id, plant_isFodder)
    return Response("{'messisFodder':'Обновлено, является ли растение кормовым.'}", status_code=200)

@router.post("/plants/update/isExactingToTheLight", tags=["PlantController"])
async def plants_post_update_isExactingToTheLight(plant_id: int, plant_isExactingToTheLight: int):
    """
      Описание: изменение того, является растение требовательным к свету или нет.
      Ограничения: растение может быть только или нетребовательным к свету (0), или требовательным к свету (1).
    """
    conn = get_db_connection()
    if ((plant_isExactingToTheLight < 0) or (plant_isExactingToTheLight > 1)):
        raise HTTPException(status_code=400, detail="Ошибка: растение может быть только или нетребовательным к свету (0), или требовательным к свету (1).")
    x = update_plant_isExactingToTheLight(conn, plant_id, plant_isExactingToTheLight)
    return Response("{'messisExactingToTheLight':'Обновлено, является ли растение требовательным к свету.'}", status_code=200)

@router.post("/plants/update/isOneYear", tags=["PlantController"])
async def plants_post_update_isOneYear(plant_id: int, plant_isOneYear: int):
    """
      Описание: изменение того, является растение однолетним или нет.
      Ограничения: растение может быть только или неоднолетним (0), или однолетним (1).
    """
    conn = get_db_connection()
    if ((plant_isOneYear < 0) or (plant_isOneYear > 1)):
        raise HTTPException(status_code=400, detail="Ошибка: растение может быть только или неоднолетним (0), или однолетним (1).")
    x = update_plant_isOneYear(conn, plant_id, plant_isOneYear)
    return Response("{'messisOneYear':'Обновлено, является ли растение однолетним.'}", status_code=200)

@router.post("/plants/update/isTwoYears", tags=["PlantController"])
async def plants_post_update_isTwoYears(plant_id: int, plant_isTwoYears: int):
    """
      Описание: изменение того, является растение двухлетним или нет.
      Ограничения: растение может быть только или недвухлетним (0), или двухлетним (1).
    """
    conn = get_db_connection()
    if ((plant_isTwoYears < 0) or (plant_isTwoYears > 1)):
        raise HTTPException(status_code=400, detail="Ошибка: растение может быть только или недвухлетним (0), или двухлетним (1).")
    x = update_plant_isTwoYears(conn, plant_id, plant_isTwoYears)
    return Response("{'messisTwoYears':'Обновлено, является ли растение двухлетним.'}", status_code=200)

@router.post("/plants/update/isManyYears", tags=["PlantController"])
async def plants_post_update_isManyYears(plant_id: int, plant_isManyYears: int):
    """
      Описание: изменение того, является растение многолетним или нет.
      Ограничения: растение может быть только или немноголетним (0), или многолетним (1).
    """
    conn = get_db_connection()
    if ((plant_isManyYears < 0) or (plant_isManyYears > 1)):
        raise HTTPException(status_code=400, detail="Ошибка: растение может быть только или немноголетним (0), или многолетним (1).")
    x = update_plant_isManyYears(conn, plant_id, plant_isManyYears)
    return Response("{'messisManyYears':'Обновлено, является ли растение многолетним.'}", status_code=200)

@router.post("/plants/update/climat", tags=["PlantController"])
async def plants_post_update_climat(plant_id: int, plant_climat: str):
    """
      Описание: изменение подходящего для растения климата.
      Ограничения: краткое описание подходящего для растения климата должно иметь длину не более 50 символов.
    """
    conn = get_db_connection()
    if ((len(plant_climat) > 50)):
        raise HTTPException(status_code=400, detail="Ошибка: краткое описание подходящего для растения климата должно иметь длину не более 50 символов.")
    x = update_plant_climat(conn, plant_id, plant_climat)
    return Response("{'messclimat':'Подходящий для растения климат обновлён.'}", status_code=200)

@router.post("/plants/update/requiredmineralsandtraceelements", tags=["PlantController"])
async def plants_post_update_required_minerals_and_trace_elements(plant_id: int, plant_required_minerals_and_trace_elements: str):
    """
      Описание: изменение перечня требуемых для растения минералов и микроэлементов.
      Ограничения: перечень требуемых для растения минералов и микроэлементов должен иметь длину не более 300 символов.
    """
    conn = get_db_connection()
    if ((len(plant_required_minerals_and_trace_elements) > 300)):
        raise HTTPException(status_code=400, detail="Ошибка: перечень требуемых для растения минералов и микроэлементов должен иметь длину не более 300 символов.")
    x = update_plant_required_minerals_and_trace_elements(conn, plant_id, plant_required_minerals_and_trace_elements)
    return Response("{'messrequiredmineralsandtraceelements':'Перечень требуемых для растения минералов и микроэлементов обновлён.'}", status_code=200)

@router.post("/plants/update/temperaturemin", tags=["PlantController"])
async def plants_post_update_temperature_min(plant_id: int, plant_temperature_min: int):
    """
      Описание: изменение минимальной подходящей для растения температуры.
      Ограничения: 1) минимальная подходящая для растения температура должна принадлежать интервалу [-100; 100];
                   2) минимальная подходящая для растения температура всегда должна быть меньше или равна максимальной.
    """
    conn = get_db_connection()
    if ((plant_temperature_min < -100) or (plant_temperature_min > 100)):
        raise HTTPException(status_code=400, detail="Ошибка: минимальная подходящая для растения температура должна принадлежать интервалу [-100; 100].")
    y = check_one_plants_temperature_min_max_min(conn, plant_id, plant_temperature_min)
    if len(y) == 0:
        raise HTTPException(status_code=400, detail="Ошибка: минимальная подходящая для растения температура всегда должна быть меньше или равна максимальной.")
    x = update_plant_temperature_min(conn, plant_id, plant_temperature_min)
    return Response("{'messtemperaturemin':'Минимальная подходящая для растения температура обновлена.'}", status_code=200)

@router.post("/plants/update/temperaturemax", tags=["PlantController"])
async def plants_post_update_temperature_max(plant_id: int, plant_temperature_max: int):
    """
      Описание: изменение максимальной подходящей для растения температуры.
      Ограничения: 1) максимальная подходящая для растения температура должна принадлежать интервалу [-100; 100];
                   2) максимальная подходящая для растения температура всегда должна быть больше или равна минимальной.
    """
    conn = get_db_connection()
    if ((plant_temperature_max < -100) or (plant_temperature_max > 100)):
        raise HTTPException(status_code=400, detail="Ошибка: максимальная подходящая для растения температура должна принадлежать интервалу [-100; 100].")
    y = check_one_plants_temperature_min_max_max(conn, plant_id, plant_temperature_max)
    if len(y) == 0:
        raise HTTPException(status_code=400, detail="Ошибка: максимальная подходящая для растения температура всегда должна быть больше или равна минимальной.")
    x = update_plant_temperature_max(conn, plant_id, plant_temperature_max)
    return Response("{'messtemperaturemax':'Максимальная подходящая для растения температура обновлена.'}", status_code=200)

@router.post("/plants/update/kingdom", tags=["PlantController"])
async def plants_post_update_kingdom(plant_id: int, plant_kingdom: str):
    """
      Описание: изменение царства растения.
      Ограничения: длина названия царства растения должна быть <= 30 символов.
    """
    conn = get_db_connection()
    if ((len(plant_kingdom) > 30)):
        raise HTTPException(status_code=400, detail="Ошибка: название царства растения должно иметь длину не более 30 символов.")
    x = update_plant_kingdom(conn, plant_id, plant_kingdom)
    return Response("{'messkingdom':'Царство растения обновлено.'}", status_code=200)

@router.post("/plants/update/philum", tags=["PlantController"])
async def plants_post_update_philum(plant_id: int, plant_philum: str):
    """
      Описание: изменение типа растения.
      Ограничения: длина названия типа растения должна быть <= 30 символов.
    """
    conn = get_db_connection()
    if ((len(plant_philum) > 30)):
        raise HTTPException(status_code=400, detail="Ошибка: название типа растения должно иметь длину не более 30 символов.")
    x = update_plant_philum(conn, plant_id, plant_philum)
    return Response("{'messphilum':'Тип растения обновлён.'}", status_code=200)

@router.post("/plants/update/class", tags=["PlantController"])
async def plants_post_update_class(plant_id: int, plant_class: str):
    """
      Описание: изменение класса растения.
      Ограничения: длина названия класса растения должна быть <= 30 символов.
    """
    conn = get_db_connection()
    if ((len(plant_class) > 30)):
        raise HTTPException(status_code=400, detail="Ошибка: название класса растения должно иметь длину не более 30 символов.")
    x = update_plant_class(conn, plant_id, plant_class)
    return Response("{'messclass':'Класс растения обновлён.'}", status_code=200)

@router.post("/plants/update/order", tags=["PlantController"])
async def plants_post_update_order(plant_id: int, plant_order: str):
    """
      Описание: изменение порядка растения.
      Ограничения: длина названия порядка растения должна быть <= 30 символов.
    """
    conn = get_db_connection()
    if ((len(plant_order) > 30)):
        raise HTTPException(status_code=400, detail="Ошибка: название порядка растения должно иметь длину не более 30 символов.")
    x = update_plant_order(conn, plant_id, plant_order)
    return Response("{'messorder':'Порядок растения обновлён.'}", status_code=200)

@router.post("/plants/update/family", tags=["PlantController"])
async def plants_post_update_family(plant_id: int, plant_family: str):
    """
      Описание: изменение семейства растения.
      Ограничения: длина названия семейства растения должна быть <= 30 символов.
    """
    conn = get_db_connection()
    if ((len(plant_family) > 30)):
        raise HTTPException(status_code=400, detail="Ошибка: название семейства растения должно иметь длину не более 30 символов.")
    x = update_plant_family(conn, plant_id, plant_family)
    return Response("{'messfamily':'Семейство растения обновлено.'}", status_code=200)

@router.post("/plants/update/genus", tags=["PlantController"])
async def plants_post_update_genus(plant_id: int, plant_genus: str):
    """
      Описание: изменение рода растения.
      Ограничения: длина названия рода растения должна быть <= 30 символов.
    """
    conn = get_db_connection()
    if ((len(plant_genus) > 30)):
        raise HTTPException(status_code=400, detail="Ошибка: название рода растения должно иметь длину не более 30 символов.")
    x = update_plant_genus(conn, plant_id, plant_genus)
    return Response("{'messgenus':'Родовая принадлежность растения обновлена.'}", status_code=200)

@router.post("/plants/update/species", tags=["PlantController"])
async def plants_post_update_species(plant_id: int, plant_species: str):
    """
      Описание: изменение вида растения.
      Ограничения: длина названия вида растения должна быть <= 30 символов.
    """
    conn = get_db_connection()
    if ((len(plant_species) > 30)):
        raise HTTPException(status_code=400, detail="Ошибка: название вида растения должно иметь длину не более 30 символов.")
    x = update_plant_species(conn, plant_id, plant_species)
    return Response("{'messspecies':'Видовая принадлежность растения обновлена.'}", status_code=200)

@router.post("/plants/update/picture", tags=["PlantController"])
async def plants_post_update_picture(plant: Plant.PlantPicture):
    """
      Описание: изменение картинки растения.
      Ограничения: длина содержимого файла с картинкой должна быть <= 10000000 символов.
    """
    conn = get_db_connection()
    if ((len(plant.plant_picture) > 10000000)):
        raise HTTPException(status_code=400, detail="Ошибка: содержимое файла с картинкой должно иметь длину не более 10000000 символов.")
    x = update_plant_picture(conn, plant.plant_id, plant.plant_picture)
    return Response("{'messpicture':'Картинка растения обновлена.'}", status_code=200)

@router.get("/plants/get/picture", tags=["PlantController"])
async def plants_get_picture(plant_id: int):
    """
      Описание: получение картинки растения.
    """
    conn = get_db_connection()
    x = get_plant_picture(conn, plant_id)
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False), status_code=200)
