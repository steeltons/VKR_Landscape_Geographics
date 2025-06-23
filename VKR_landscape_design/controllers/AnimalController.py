from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, Response, HTTPException
import json
from base_models import Animal
from models.animals_model import *
from utils import get_db_connection
router = APIRouter()



@router.get("/animals/all", tags=["AnimalController"])
async def animals_get_select_all():
    """
      Описание: получение данных обо всех животных.
    """
    conn = get_db_connection()
    x = get_animals(conn)
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"), status_code=200)

@router.get("/animals/one", tags=["AnimalController"])
async def animals_get_one_animal(animal_id: int):
    """
      Описание: получение данных об одном животном по его ID (кроме картинки).
    """
    conn = get_db_connection()
    x = get_one_animal(conn, animal_id)
    if len(x) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: животное с данным ID не найдено.")
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False), status_code=200)

@router.post("/animals/delete", tags=["AnimalController"])
async def animals_post_delete(animal_id: int):
    """
      Описание: удаление животного по его ID.
    """
    conn = get_db_connection()
    y = get_one_animal(conn, animal_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: животное с данным ID не найдено, потому удалить его невозможно.")
    x = delete_animal(conn, animal_id)
    return Response("{'messdelete':'Животное удалёно.'}", status_code=200)

@router.post("/animals/insert", tags=["AnimalController"])
async def animals_post_insert(animal_name: str, animal_description: str):
    """
      Описание: добавление животного. На ввод подаются название и описание.
      Ограничения: 1) длина названия животного должна быть <= 30 символов, и название не должно быть пустым;
                   2) длина описания животного должна быть <= 3000 символов, и описание не должно быть пустым;
                   3) название животного должно быть уникальным (повторы не допускаются).
    """
    conn = get_db_connection()
    if ((len(animal_name) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: название животного не должно быть пустым.")
    if ((len(animal_description) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: описание животного не должно быть пустым.")
    if ((len(animal_name) > 30)):
        raise HTTPException(status_code=400, detail="Ошибка: название животного должно иметь длину не более 30 символов.")
    if ((len(animal_description) > 3000)):
        raise HTTPException(status_code=400, detail="Ошибка: описание животного должно иметь длину не более 3000 символов.")
    y = find_animal_name(conn, animal_name)
    if len(y) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: в базе данных уже есть животное с таким названием.")
    x = insert_animal(conn, animal_name, animal_description)
    return Response("{'messinsert':'Животное создано.'}", status_code=200)

@router.post("/animals/update/name", tags=["AnimalController"])
async def animals_post_update_name(animal_id: int, animal_name: str):
    """
      Описание: изменение названия животного.
      Ограничения: длина названия животного должна быть <= 30 символов, и название не должно быть пустым.
    """
    conn = get_db_connection()
    if ((len(animal_name) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: название почвы не должно быть пустым.")
    if ((len(animal_name) > 30)):
        raise HTTPException(status_code=400, detail="Ошибка: название животного должно иметь длину не более 30 символов.")
    x = update_animal_name(conn, animal_id, animal_name)
    return Response("{'messname':'Название животного обновлено.'}", status_code=200)

@router.post("/animals/update/description", tags=["AnimalController"])
async def animals_post_update_description(animal_id: int, animal_description: str):
    """
      Описание: изменение описания животного.
      Ограничения: длина описания животного должна быть <= 3000 символов, и описание не должно быть пустым.
    """
    conn = get_db_connection()
    if ((len(animal_description) == 0)):
        raise HTTPException(status_code=400, detail="Ошибка: описание почвы не должно быть пустым.")
    if ((len(animal_description) > 3000)):
        raise HTTPException(status_code=400, detail="Ошибка: описание животного должно иметь длину не более 3000 символов.")
    x = update_animal_description(conn, animal_id, animal_description)
    return Response("{'messdescription':'Описание животного обновлено.'}", status_code=200)

@router.post("/animals/update/kingdom", tags=["AnimalController"])
async def animals_post_update_kingdom(animal_id: int, animal_kingdom: str):
    """
      Описание: изменение царства животного.
      Ограничения: длина названия царства животного должна быть <= 30 символов.
    """
    conn = get_db_connection()
    if ((len(animal_kingdom) > 30)):
        raise HTTPException(status_code=400, detail="Ошибка: название царства животного должно иметь длину не более 30 символов.")
    x = update_animal_kingdom(conn, animal_id, animal_kingdom)
    return Response("{'messkingdom':'Царство животного обновлено.'}", status_code=200)

@router.post("/animals/update/philum", tags=["AnimalController"])
async def animals_post_update_philum(animal_id: int, animal_philum: str):
    """
      Описание: изменение типа животного.
      Ограничения: длина названия типа животного должна быть <= 30 символов.
    """
    conn = get_db_connection()
    if ((len(animal_philum) > 30)):
        raise HTTPException(status_code=400, detail="Ошибка: название типа животного должно иметь длину не более 30 символов.")
    x = update_animal_philum(conn, animal_id, animal_philum)
    return Response("{'messphilum':'Тип животного обновлён.'}", status_code=200)

@router.post("/animals/update/class", tags=["AnimalController"])
async def animals_post_update_class(animal_id: int, animal_class: str):
    """
      Описание: изменение класса животного.
      Ограничения: длина названия класса животного должна быть <= 30 символов.
    """
    conn = get_db_connection()
    if ((len(animal_class) > 30)):
        raise HTTPException(status_code=400, detail="Ошибка: название класса животного должно иметь длину не более 30 символов.")
    x = update_animal_class(conn, animal_id, animal_class)
    return Response("{'messclass':'Класс животного обновлён.'}", status_code=200)

@router.post("/animals/update/order", tags=["AnimalController"])
async def animals_post_update_order(animal_id: int, animal_order: str):
    """
      Описание: изменение порядка животного.
      Ограничения: длина названия порядка животного должна быть <= 30 символов.
    """
    conn = get_db_connection()
    if ((len(animal_order) > 30)):
        raise HTTPException(status_code=400, detail="Ошибка: название порядка животного должно иметь длину не более 30 символов.")
    x = update_animal_order(conn, animal_id, animal_order)
    return Response("{'messorder':'Порядок животного обновлён.'}", status_code=200)

@router.post("/animals/update/family", tags=["AnimalController"])
async def animals_post_update_family(animal_id: int, animal_family: str):
    """
      Описание: изменение семейства животного.
      Ограничения: длина названия семейства животного должна быть <= 30 символов.
    """
    conn = get_db_connection()
    if ((len(animal_family) > 30)):
        raise HTTPException(status_code=400, detail="Ошибка: название семейства животного должно иметь длину не более 30 символов.")
    x = update_animal_family(conn, animal_id, animal_family)
    return Response("{'messfamily':'Семейство животного обновлено.'}", status_code=200)

@router.post("/animals/update/genus", tags=["AnimalController"])
async def animals_post_update_genus(animal_id: int, animal_genus: str):
    """
      Описание: изменение рода животного.
      Ограничения: длина названия рода животного должна быть <= 30 символов.
    """
    conn = get_db_connection()
    if ((len(animal_genus) > 30)):
        raise HTTPException(status_code=400, detail="Ошибка: название рода животного должно иметь длину не более 30 символов.")
    x = update_animal_genus(conn, animal_id, animal_genus)
    return Response("{'messgenus':'Родовая принадлежность животного обновлена.'}", status_code=200)

@router.post("/animals/update/species", tags=["AnimalController"])
async def animals_post_update_species(animal_id: int, animal_species: str):
    """
      Описание: изменение вида животного.
      Ограничения: длина названия вида животного должна быть <= 30 символов.
    """
    conn = get_db_connection()
    if ((len(animal_species) > 30)):
        raise HTTPException(status_code=400, detail="Ошибка: название вида животного должно иметь длину не более 30 символов.")
    x = update_animal_species(conn, animal_id, animal_species)
    return Response("{'messspecies':'Видовая принадлежность животного обновлена.'}", status_code=200)

@router.post("/animals/update/picture", tags=["AnimalController"])
async def animals_post_update_picture(animal: Animal.AnimalPicture):
    """
      Описание: изменение картинки животного.
      Ограничения: длина содержимого файла с картинкой должна быть <= 10000000 символов.
    """
    conn = get_db_connection()
    if ((len(animal.animal_picture) > 10000000)):
        raise HTTPException(status_code=400, detail="Ошибка: содержимое файла с картинкой должно иметь длину не более 10000000 символов.")
    x = update_animal_picture(conn, animal.animal_id, animal.animal_picture)
    return Response("{'messpicture':'Картинка животного обновлена.'}", status_code=200)

@router.get("/animals/get/picture", tags=["AnimalController"])
async def animals_get_picture(animal_id: int):
    """
      Описание: получение картинки животного.
    """
    conn = get_db_connection()
    y = get_one_animal(conn, animal_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: животное с данным ID не найдено, потому получить его картинку невозможно.")
    x = get_animal_picture(conn, animal_id)
    return Response(json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False), status_code=200)
