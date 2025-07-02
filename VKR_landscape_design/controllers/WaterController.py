from fastapi import APIRouter, Response, HTTPException
import json
from models.waters_model import *
from utils import get_db_connection
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils import get_db_connection
from controllers.UserController import get_current_active_admin_user

router = APIRouter()
security = HTTPBearer()

water_example = {
    "water_id": 1,
    "water_name": "Вода",
    "water_description": "Описание воды",
    "water_picture_id": 1,
    "water_picture_base64": "base64_encoded_string_for_water"
}

water_list_example = [
    {
        "water_id": 1,
        "water_name": "Вода",
        "water_description": "Описание воды",
        "water_picture_id": 1,
        "water_picture_base64": "base64_encoded_string_for_water"
    },
    {
        "water_id": 2,
        "water_name": "Вода",
        "water_description": "Описание воды",
        "water_picture_id": 1,
        "water_picture_base64": "base64_encoded_string_for_water"
    }
]

@router.get("/waters/all", tags=["WaterController"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "Example response with pictures": {
                        "value": water_list_example
                    }
                }
            }
        }
    },
    400: {
        "description": "Invalid input parameters",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: недопустимые параметры пагинации или поиска."}
            }
        }
    }
})
async def waters_get_select_all(
    is_need_pictures: bool = False,
    search_query: str | None = None,
    page: int | None = None,
    elements: int | None = None
):
    """Описание: получение данных обо всех водах с поддержкой пагинации и поиска."""
    if page is not None and page < 1:
        raise HTTPException(status_code=400, detail="Ошибка: номер страницы должен быть положительным числом.")
    if elements is not None and elements < 1:
        raise HTTPException(status_code=400, detail="Ошибка: количество объектов на странице должно быть положительным числом.")

    conn = get_db_connection()
    x = get_waters(conn, is_need_pictures, search_query, page, elements)
    return Response(
        json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"),
        status_code=200
    )


@router.get("/waters/one", tags=["WaterController"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "Example response with picture": {
                        "value": water_example
                    }
                }
            }
        }
    },
    404: {
        "description": "Water not found",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: вода с данным ID не найдена."}
            }
        }
    }
})
async def waters_get_one_water(water_id: int, is_need_pictures: bool = False):
    """Описание: получение данных об одной воде по её идентификатору."""
    conn = get_db_connection()
    x = get_one_water(conn, water_id, is_need_pictures)
    if len(x) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: вода с данным ID не найдена.")
    return Response(
        json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"),
        status_code=200
    )

@router.delete("/waters/delete", tags=["WaterController"], responses={
    200: {
        "description": "Water deleted successfully",
        "content": {
            "application/json": {
                "example": {"message": "Вода удалена."}
            }
        }
    },
    404: {
        "description": "Water not found",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: вода с данным ID не найдена, потому удалить её невозможно."}
            }
        }
    }
})
async def waters_delete(water_id: int,
    current_user: dict = Depends(get_current_active_admin_user)):
    """Описание: удаление воды по её ID."""
    conn = get_db_connection()
    y = get_one_water(conn, water_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: вода с данным ID не найдена, потому удалить её невозможно.")
    x = delete_water(conn, water_id)
    return Response("{'message':'Вода удалена.'}", status_code=200)

@router.post("/waters/insert", tags=["WaterController"], responses={
    200: {
        "description": "Water created successfully",
        "content": {
            "application/json": {
                "example": {"message": "Вода создана."}
            }
        }
    },
    400: {
        "description": "Invalid input data",
        "content": {
            "application/json": {
                "examples": {
                    "Empty name": {
                        "value": {"detail": "Ошибка: название воды не должно быть пустым."}
                    },
                    "Name too long": {
                        "value": {"detail": "Ошибка: длина названия должна быть меньше или равна 30 символов."}
                    },
                    "Description too long": {
                        "value": {"detail": "Ошибка: длина описания должна быть меньше или равна 3000 символов."}
                    },
                    "Invalid picture ID": {
                        "value": {"detail": "Ошибка: идентификатор картинки должен быть больше 0."}
                    },
                    "Duplicate name": {
                        "value": {"detail": "Ошибка: название должно быть уникальным (повторы не допускаются)."}
                    }
                }
            }
        }
    }
})
async def waters_insert(water_name: str, water_description: str | None = None, water_picture_id: int | None = None,
    current_user: dict = Depends(get_current_active_admin_user)):
    """Описание: добавление воды. На ввод подаются название, описание и идентификатор картинки."""
    conn = get_db_connection()
    if water_name is not None and len(water_name) == 0:
        raise HTTPException(status_code=400, detail="Ошибка: название воды не должно быть пустым.")
    if water_name is not None and len(water_name) > 30:
        raise HTTPException(status_code=400, detail="Ошибка: длина названия должна быть меньше или равна 30 символов.")
    if water_description is not None and len(water_description) > 3000:
        raise HTTPException(status_code=400, detail="Ошибка: длина описания должна быть меньше или равна 3000 символов.")
    if len(find_water_name(conn, water_name)) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: название должно быть уникальным (повторы не допускаются).")
    x = insert_water(conn, water_name, water_description, water_picture_id)
    return Response("{'message':'Вода создана.'}", status_code=200)

@router.patch("/waters/update", tags=["WaterController"], responses={
    200: {
        "description": "Water updated successfully",
        "content": {
            "application/json": {
                "example": {"message": "Вода обновлена."}
            }
        }
    },
    400: {
        "description": "Invalid input data",
        "content": {
            "application/json": {
                "examples": {
                    "Empty name": {
                        "value": {"detail": "Ошибка: название воды не должно быть пустым."}
                    },
                    "Name too long": {
                        "value": {"detail": "Ошибка: длина названия должна быть меньше или равна 30 символов."}
                    },
                    "Description too long": {
                        "value": {"detail": "Ошибка: длина описания должна быть меньше или равна 3000 символов."}
                    },
                    "Invalid picture ID": {
                        "value": {"detail": "Ошибка: идентификатор картинки должен быть больше 0."}
                    },
                    "Duplicate name": {
                        "value": {"detail": "Ошибка: название должно быть уникальным (повторы не допускаются)."}
                    }
                }
            }
        }
    }
})
async def waters_update(water_id: int, water_name: str | None = None, water_description: str | None = None, water_picture_id: int | None = None,
    current_user: dict = Depends(get_current_active_admin_user)):
    """Описание: изменение параметров воды. На ввод подаются идентификатор, название, описание и идентификатор картинки."""
    conn = get_db_connection()
    if water_name is not None and len(water_name) == 0:
        raise HTTPException(status_code=400, detail="Ошибка: название воды не должно быть пустым.")
    if water_name is not None and len(water_name) > 30:
        raise HTTPException(status_code=400, detail="Ошибка: длина названия должна быть меньше или равна 30 символов.")
    if water_description is not None and len(water_description) > 3000:
        raise HTTPException(status_code=400, detail="Ошибка: длина описания должна быть меньше или равна 3000 символов.")
    if len(find_water_name_with_id(conn, water_id, water_name)) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: название должно быть уникальным (повторы не допускаются).")
    x = update_water(conn, water_id, water_name, water_description, water_picture_id)
    return Response("{'message':'Вода обновлена.'}", status_code=200)
