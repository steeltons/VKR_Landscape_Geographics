from fastapi import APIRouter, Response, HTTPException
import json

from starlette.responses import JSONResponse

from models.plants_model import *
from utils import get_db_connection
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils import get_db_connection
from controllers.UserController import get_current_active_admin_user
from pydantic import BaseModel
from fastapi import Body

router = APIRouter()
security = HTTPBearer()

plant_example = {
    "plant_id": 1,
    "plant_name": "Растение",
    "plant_description": "Описание растения",
    "plant_picture_id": 1,
    "plant_picture_base64": "base64_encoded_string_for_plant"
}

plant_list_example = [
    {
        "plant_id": 1,
        "plant_name": "Растение",
        "plant_description": "Описание растения",
        "plant_picture_id": 1,
        "plant_picture_base64": "base64_encoded_string_for_plant"
    },
    {
        "plant_id": 2,
        "plant_name": "Растение",
        "plant_description": "Описание растения",
        "plant_picture_id": 1,
        "plant_picture_base64": "base64_encoded_string_for_plant"
    }
]

@router.get("/plants/all", tags=["PlantController"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "Example response with pictures": {
                        "value": plant_list_example
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
async def plants_get_select_all(
    is_need_pictures: bool = False,
    search_query: str | None = None,
    page: int | None = None,
    elements: int | None = None
):
    """Описание: получение данных обо всех растениях с поддержкой пагинации и поиска."""
    if page is not None and page < 1:
        raise HTTPException(status_code=400, detail="Ошибка: номер страницы должен быть положительным числом.")
    if elements is not None and elements < 1:
        raise HTTPException(status_code=400, detail="Ошибка: количество объектов на странице должно быть положительным числом.")

    conn = get_db_connection()
    x = get_plants(conn, is_need_pictures, search_query, page, elements)
    return Response(
        json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"),
        status_code=200
    )


@router.get("/plants/one", tags=["PlantController"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "Example response with picture": {
                        "value": plant_example
                    }
                }
            }
        }
    },
    404: {
        "description": "Plant not found",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: растение с данным ID не найдено."}
            }
        }
    }
})
async def plants_get_one_plant(plant_id: int, is_need_pictures: bool = False):
    """Описание: получение данных об одном растении по его идентификатору."""
    conn = get_db_connection()
    x = get_one_plant(conn, plant_id, is_need_pictures)
    if len(x) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: растение с данным ID не найдено.")
    return Response(
        json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"),
        status_code=200
    )

@router.delete("/plants/delete", tags=["PlantController"], responses={
    200: {
        "description": "Plant deleted successfully",
        "content": {
            "application/json": {
                "example": {"message": "Растение удалено."}
            }
        }
    },
    404: {
        "description": "Plant not found",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: растение с данным ID не найдено, потому удалить его невозможно."}
            }
        }
    }
})
async def plants_delete(plant_id: int,
    current_user: dict = Depends(get_current_active_admin_user)):
    """Описание: удаление растения по его ID."""
    conn = get_db_connection()
    y = get_one_plant(conn, plant_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: растение с данным ID не найдено, потому удалить его невозможно.")
    x = delete_plant(conn, plant_id)
    return Response("{'message':'Растение удалено.'}", status_code=200)

class PlantInsertDto(BaseModel):
    plant_name: str
    plant_description: str | None = None
    plant_picture_id: int | None = None

@router.post("/plants/insert", tags=["PlantController"], responses={
    200: {
        "description": "Plant created successfully",
        "content": {
            "application/json": {
                "example": {"message": "Растение создано."}
            }
        }
    },
    400: {
        "description": "Invalid input data",
        "content": {
            "application/json": {
                "examples": {
                    "Empty name": {
                        "value": {"detail": "Ошибка: название растения не должно быть пустым."}
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
async def plants_insert(plant_data: PlantInsertDto = Body(...)):
    """Добавление растения через тело запроса."""
    conn = get_db_connection()
    if not plant_data.plant_name:
        raise HTTPException(status_code=400, detail=__create_error_message("Ошибка: название растения не должно быть пустым."))
    if len(plant_data.plant_name) > 30:
        raise HTTPException(status_code=400, detail=__create_error_message("Ошибка: длина названия должна быть меньше или равна 30 символов."))
    if plant_data.plant_description and len(plant_data.plant_description) > 3000:
        raise HTTPException(status_code=400, detail=__create_error_message("Ошибка: длина описания должна быть меньше или равна 3000 символов."))
    if len(find_plant_name(conn, plant_data.plant_name)) != 0:
        raise HTTPException(status_code=400, detail=__create_error_message("Ошибка: название должно быть уникальным (повторы не допускаются)."))

    insert_plant(conn, plant_data.plant_name, plant_data.plant_description, plant_data.plant_picture_id)
    return JSONResponse(content={'message': 'Растение создано.'}, status_code=200)

@router.patch("/plants/update", tags=["PlantController"], responses={
    200: {
        "description": "Plant updated successfully",
        "content": {
            "application/json": {
                "example": {"message": "Растение обновлено."}
            }
        }
    },
    400: {
        "description": "Invalid input data",
        "content": {
            "application/json": {
                "examples": {
                    "Empty name": {
                        "value": {"detail": "Ошибка: название растения не должно быть пустым."}
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
async def plants_update(plant_id: int, plant_name: str | None = None, plant_description: str | None = None, plant_picture_id: int | None = None,
    current_user: dict = Depends(get_current_active_admin_user)):
    """Описание: изменение параметров растения. На ввод подаются идентификатор, название, описание и идентификатор картинки."""
    conn = get_db_connection()
    if plant_name is not None and len(plant_name) == 0:
        raise HTTPException(status_code=400, detail=__create_error_message("Ошибка: название растения не должно быть пустым."))
    if plant_name is not None and len(plant_name) > 30:
        raise HTTPException(status_code=400, detail=__create_error_message("Ошибка: длина названия должна быть меньше или равна 30 символов."))
    if plant_description is not None and len(plant_description) > 3000:
        raise HTTPException(status_code=400, detail=__create_error_message("Ошибка: длина описания должна быть меньше или равна 3000 символов."))
    if len(find_plant_name_with_id(conn, plant_id, plant_name)) != 0:
        raise HTTPException(status_code=400, detail=__create_error_message("Ошибка: название должно быть уникальным (повторы не допускаются)."))
    x = update_plant(conn, plant_id, plant_name, plant_description, plant_picture_id)
    return JSONResponse(content={"message" : "Растение обновлено."}, status_code=200)

def __create_error_message (message: str):
    return  {
        'detail': message
    }

