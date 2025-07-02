from fastapi import APIRouter, Response, HTTPException
import json
from models.reliefs_model import *
from utils import get_db_connection
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils import get_db_connection
from controllers.UserController import get_current_active_admin_user

router = APIRouter()
security = HTTPBearer()

relief_example = {
    "relief_id": 1,
    "relief_name": "Рельеф",
    "relief_description": "Описание рельефа",
    "relief_picture_id": 1,
    "relief_picture_base64": "base64_encoded_string_for_relief"
}


relief_list_example = [
    {
        "relief_id": 1,
        "relief_name": "Рельеф",
        "relief_description": "Описание рельефа",
        "relief_picture_id": 1,
        "relief_picture_base64": "base64_encoded_string_for_relief"
    },
    {
        "relief_id": 2,
        "relief_name": "Рельеф",
        "relief_description": "Описание рельефа",
        "relief_picture_id": 1,
        "relief_picture_base64": "base64_encoded_string_for_relief"
    }
]

@router.get("/reliefs/all", tags=["ReliefController"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "Example response with pictures": {
                        "value": relief_list_example
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
async def reliefs_get_select_all(
    is_need_pictures: bool = False,
    search_query: str | None = None,
    page: int | None = None,
    elements: int | None = None
):
    """Описание: получение данных обо всех рельефах с поддержкой пагинации и поиска."""
    if page is not None and page < 1:
        raise HTTPException(status_code=400, detail="Ошибка: номер страницы должен быть положительным числом.")
    if elements is not None and elements < 1:
        raise HTTPException(status_code=400, detail="Ошибка: количество объектов на странице должно быть положительным числом.")

    conn = get_db_connection()
    x = get_reliefs(conn, is_need_pictures, search_query, page, elements)
    return Response(
        json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"),
        status_code=200
    )


@router.get("/reliefs/one", tags=["ReliefController"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "Example response with picture": {
                        "value": relief_example
                    }
                }
            }
        }
    },
    404: {
        "description": "Relief not found",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: рельеф с данным ID не найден."}
            }
        }
    }
})
async def reliefs_get_one_relief(relief_id: int, is_need_pictures: bool = False):
    """Описание: получение данных об одном рельефе по его идентификатору."""
    conn = get_db_connection()
    x = get_one_relief(conn, relief_id, is_need_pictures)
    if len(x) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: рельеф с данным ID не найден.")
    return Response(
        json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"),
        status_code=200
    )

@router.delete("/reliefs/delete", tags=["ReliefController"], responses={
    200: {
        "description": "Relief deleted successfully",
        "content": {
            "application/json": {
                "example": {"message": "Рельеф удалён."}
            }
        }
    },
    404: {
        "description": "Relief not found",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: рельеф с данным ID не найден, потому удалить его невозможно."}
            }
        }
    }
})
async def reliefs_delete(relief_id: int,
    current_user: dict = Depends(get_current_active_admin_user)):
    """Описание: удаление рельефа по его ID."""
    conn = get_db_connection()
    y = get_one_relief(conn, relief_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: рельеф с данным ID не найден, потому удалить его невозможно.")
    x = delete_relief(conn, relief_id)
    return Response("{'message':'Рельеф удалён.'}", status_code=200)

@router.post("/reliefs/insert", tags=["ReliefController"], responses={
    200: {
        "description": "Relief created successfully",
        "content": {
            "application/json": {
                "example": {"message": "Рельеф создан."}
            }
        }
    },
    400: {
        "description": "Invalid input data",
        "content": {
            "application/json": {
                "examples": {
                    "Empty name": {
                        "value": {"detail": "Ошибка: название рельефа не должно быть пустым."}
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
async def reliefs_insert(relief_name: str, relief_description: str | None = None, relief_picture_id: int | None = None,
    current_user: dict = Depends(get_current_active_admin_user)):
    """Описание: добавление рельефа. На ввод подаются название, описание и идентификатор картинки."""
    conn = get_db_connection()
    if relief_name is not None and len(relief_name) == 0:
        raise HTTPException(status_code=400, detail="Ошибка: название рельефа не должно быть пустым.")
    if relief_name is not None and len(relief_name) > 30:
        raise HTTPException(status_code=400, detail="Ошибка: длина названия должна быть меньше или равна 30 символов.")
    if relief_description is not None and len(relief_description) > 3000:
        raise HTTPException(status_code=400, detail="Ошибка: длина описания должна быть меньше или равна 3000 символов.")
    if len(find_relief_name(conn, relief_name)) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: название должно быть уникальным (повторы не допускаются).")
    x = insert_relief(conn, relief_name, relief_description, relief_picture_id)
    return Response("{'message':'Рельеф создан.'}", status_code=200)

@router.patch("/reliefs/update", tags=["ReliefController"], responses={
    200: {
        "description": "Relief updated successfully",
        "content": {
            "application/json": {
                "example": {"message": "Рельеф обновлён."}
            }
        }
    },
    400: {
        "description": "Invalid input data",
        "content": {
            "application/json": {
                "examples": {
                    "Empty name": {
                        "value": {"detail": "Ошибка: название рельефа не должно быть пустым."}
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
async def reliefs_update(relief_id: int, relief_name: str | None = None, relief_description: str | None = None, relief_picture_id: int | None = None,
    current_user: dict = Depends(get_current_active_admin_user)):
    """Описание: изменение параметров рельефа. На ввод подаются идентификатор, название, описание и идентификатор картинки."""
    conn = get_db_connection()
    if relief_name is not None and len(relief_name) == 0:
        raise HTTPException(status_code=400, detail="Ошибка: название рельефа не должно быть пустым.")
    if relief_name is not None and len(relief_name) > 30:
        raise HTTPException(status_code=400, detail="Ошибка: длина названия должна быть меньше или равна 30 символов.")
    if relief_description is not None and len(relief_description) > 3000:
        raise HTTPException(status_code=400, detail="Ошибка: длина описания должна быть меньше или равна 3000 символов.")
    if len(find_relief_name_with_id(conn, relief_id, relief_name)) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: название должно быть уникальным (повторы не допускаются).")
    x = update_relief(conn, relief_id, relief_name, relief_description, relief_picture_id)
    return Response("{'message':'Рельеф обновлён.'}", status_code=200)

