from fastapi import APIRouter, Response, HTTPException
import json
from models.grounds_model import *
from utils import get_db_connection
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils import get_db_connection
from controllers.UserController import get_current_active_admin_user

router = APIRouter()
security = HTTPBearer()

ground_example = {
    "ground_id": 1,
    "ground_name": "Грунт",
    "ground_description": "Описание грунта",
    "ground_density": 1.5,
    "ground_humidity": 0.5,
    "ground_solidity": 0.8,
    "ground_picture_id": 1,
    "ground_picture_base64": "base64_encoded_string_for_ground"
}

ground_list_example = [
    {
        "ground_id": 1,
        "ground_name": "Грунт",
        "ground_description": "Описание грунта",
        "ground_density": 1.5,
        "ground_humidity": 0.5,
        "ground_solidity": 0.8,
        "ground_picture_id": 1,
        "ground_picture_base64": "base64_encoded_string_for_ground"
    },
    {
        "ground_id": 2,
        "ground_name": "Грунт",
        "ground_description": "Описание грунта",
        "ground_density": 1.6,
        "ground_humidity": 0.4,
        "ground_solidity": 0.7,
        "ground_picture_id": 1,
        "ground_picture_base64": "base64_encoded_string_for_ground"
    }
]

@router.get("/grounds/all", tags=["GroundController"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "Example response with pictures": {
                        "value": ground_list_example
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
async def grounds_get_select_all(
    is_need_pictures: bool = False,
    search_query: str | None = None,
    page: int | None = None,
    elements: int | None = None
):
    """Описание: получение данных обо всех грунтах с поддержкой пагинации и поиска."""
    if page is not None and page < 1:
        raise HTTPException(status_code=400, detail="Ошибка: номер страницы должен быть положительным числом.")
    if elements is not None and elements < 1:
        raise HTTPException(status_code=400, detail="Ошибка: количество объектов на странице должно быть положительным числом.")

    conn = get_db_connection()
    x = get_grounds(conn, is_need_pictures, search_query, page, elements)
    return Response(
        json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"),
        status_code=200
    )


@router.get("/grounds/one", tags=["GroundController"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "Example response with picture": {
                        "value": ground_example
                    }
                }
            }
        }
    },
    404: {
        "description": "Ground not found",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: грунт с данным ID не найден."}
            }
        }
    }
})
async def grounds_get_one_ground(ground_id: int, is_need_pictures: bool = False):
    """Описание: получение данных об одном грунте по его идентификатору."""
    conn = get_db_connection()
    x = get_one_ground(conn, ground_id, is_need_pictures)
    if len(x) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: грунт с данным ID не найден.")
    return Response(
        json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False),
        status_code=200
    )

@router.delete("/grounds/delete", tags=["GroundController"], responses={
    200: {
        "description": "Ground deleted successfully",
        "content": {
            "application/json": {
                "example": {"message": "Грунт удалён."}
            }
        }
    },
    404: {
        "description": "Ground not found",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: грунт с данным ID не найден, потому удалить его невозможно."}
            }
        }
    }
})
async def grounds_delete(ground_id: int,
    current_user: dict = Depends(get_current_active_admin_user)):
    """Описание: удаление грунта по его ID."""
    conn = get_db_connection()
    y = get_one_ground(conn, ground_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: грунт с данным ID не найден, потому удалить его невозможно.")
    x = delete_ground(conn, ground_id)
    return Response("{'message':'Грунт удалён.'}", status_code=200)

@router.post("/grounds/insert", tags=["GroundController"], responses={
    200: {
        "description": "Ground created successfully",
        "content": {
            "application/json": {
                "example": {"message": "Грунт создан."}
            }
        }
    },
    400: {
        "description": "Invalid input data",
        "content": {
            "application/json": {
                "examples": {
                    "Empty name": {
                        "value": {"detail": "Ошибка: название грунта не должно быть пустым."}
                    },
                    "Name too long": {
                        "value": {"detail": "Ошибка: длина названия должна быть меньше или равна 30 символов."}
                    },
                    "Description too long": {
                        "value": {"detail": "Ошибка: длина описания должна быть меньше или равна 3000 символов."}
                    },
                    "Invalid density": {
                        "value": {"detail": "Ошибка: плотность должна быть больше 0."}
                    },
                    "Invalid humidity": {
                        "value": {"detail": "Ошибка: влажность должна быть больше 0."}
                    },
                    "Invalid solidity": {
                        "value": {"detail": "Ошибка: твердость должна быть больше 0."}
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
async def grounds_insert(ground_name: str, ground_description: str | None = None, ground_density: float | None = None, ground_humidity: float | None = None, ground_solidity: float | None = None, ground_picture_id: int | None = None,
    current_user: dict = Depends(get_current_active_admin_user)):
    """Описание: добавление грунта. На ввод подаются название, описание, плотность, влажность, твердость и идентификатор картинки."""
    conn = get_db_connection()
    if ground_name is not None and len(ground_name) == 0:
        raise HTTPException(status_code=400, detail="Ошибка: название грунта не должно быть пустым.")
    if ground_name is not None and len(ground_name) > 30:
        raise HTTPException(status_code=400, detail="Ошибка: длина названия должна быть меньше или равна 30 символов.")
    if ground_description is not None and len(ground_description) > 3000:
        raise HTTPException(status_code=400, detail="Ошибка: длина описания должна быть меньше или равна 3000 символов.")
    if ground_density is not None and ground_density < 0:
        raise HTTPException(status_code=400, detail="Ошибка: плотность должна быть больше 0.")
    if ground_humidity is not None and ground_humidity < 0:
        raise HTTPException(status_code=400, detail="Ошибка: влажность должна быть больше 0.")
    if ground_solidity is not None and ground_solidity < 0:
        raise HTTPException(status_code=400, detail="Ошибка: твердость должна быть больше 0.")
    if len(find_ground_name(conn, ground_name)) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: название должно быть уникальным (повторы не допускаются).")
    x = insert_ground(conn, ground_name, ground_description, ground_density, ground_humidity, ground_solidity, ground_picture_id)
    return Response("{'message':'Грунт создан.'}", status_code=200)

@router.patch("/grounds/update", tags=["GroundController"], responses={
    200: {
        "description": "Ground updated successfully",
        "content": {
            "application/json": {
                "example": {"message": "Грунт обновлён."}
            }
        }
    },
    400: {
        "description": "Invalid input data",
        "content": {
            "application/json": {
                "examples": {
                    "Empty name": {
                        "value": {"detail": "Ошибка: название грунта не должно быть пустым."}
                    },
                    "Name too long": {
                        "value": {"detail": "Ошибка: длина названия должна быть меньше или равна 30 символов."}
                    },
                    "Description too long": {
                        "value": {"detail": "Ошибка: длина описания должна быть меньше или равна 3000 символов."}
                    },
                    "Invalid density": {
                        "value": {"detail": "Ошибка: плотность должна быть больше 0."}
                    },
                    "Invalid humidity": {
                        "value": {"detail": "Ошибка: влажность должна быть больше 0."}
                    },
                    "Invalid solidity": {
                        "value": {"detail": "Ошибка: твердость должна быть больше 0."}
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
async def grounds_update(ground_id: int, ground_name: str | None = None, ground_description: str | None = None, ground_density: float | None = None, ground_humidity: float | None = None, ground_solidity: float | None = None, ground_picture_id: int | None = None,
    current_user: dict = Depends(get_current_active_admin_user)):
    """Описание: изменение параметров грунта. На ввод подаются идентификатор, название, описание, плотность, влажность, твердость и идентификатор картинки."""
    conn = get_db_connection()
    if ground_name is not None and len(ground_name) == 0:
        raise HTTPException(status_code=400, detail="Ошибка: название грунта не должно быть пустым.")
    if ground_name is not None and len(ground_name) > 30:
        raise HTTPException(status_code=400, detail="Ошибка: длина названия должна быть меньше или равна 30 символов.")
    if ground_description is not None and len(ground_description) > 3000:
        raise HTTPException(status_code=400, detail="Ошибка: длина описания должна быть меньше или равна 3000 символов.")
    if ground_density is not None and ground_density < 0:
        raise HTTPException(status_code=400, detail="Ошибка: плотность должна быть больше 0.")
    if ground_humidity is not None and ground_humidity < 0:
        raise HTTPException(status_code=400, detail="Ошибка: влажность должна быть больше 0.")
    if ground_solidity is not None and ground_solidity < 0:
        raise HTTPException(status_code=400, detail="Ошибка: твердость должна быть больше 0.")
    if len(find_ground_name_with_id(conn, ground_id, ground_name)) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: название должно быть уникальным (повторы не допускаются).")
    x = update_ground(conn, ground_id, ground_name, ground_description, ground_density, ground_humidity, ground_solidity, ground_picture_id)
    return Response("{'message':'Грунт обновлён.'}", status_code=200)
