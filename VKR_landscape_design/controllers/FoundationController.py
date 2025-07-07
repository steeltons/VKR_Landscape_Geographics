from fastapi import APIRouter, Response, HTTPException
import json
from models.foundations_model import *
from utils import get_db_connection
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils import get_db_connection
from controllers.UserController import get_current_active_admin_user
from starlette.responses import JSONResponse

router = APIRouter()
security = HTTPBearer()

foundation_example = {
    "foundation_id": 1,
    "foundation_name": "Фундамент",
    "foundation_description": "Описание фундамента",
    "foundation_depth_roof_root_in_meters": 2.0,
    "foundation_picture_id": 1,
    "foundation_picture_base64": "base64_encoded_string_for_foundation"
}


foundation_list_example = [
    {
        "foundation_id": 1,
        "foundation_name": "Фундамент",
        "foundation_description": "Описание фундамента",
        "foundation_depth_roof_root_in_meters": 2.0,
        "foundation_picture_id": 1,
        "foundation_picture_base64": "base64_encoded_string_for_foundation"
    },
    {
        "foundation_id": 2,
        "foundation_name": "Фундамент",
        "foundation_description": "Описание фундамента",
        "foundation_depth_roof_root_in_meters": 2.0,
        "foundation_picture_id": 1,
        "foundation_picture_base64": "base64_encoded_string_for_foundation"
    }
]

@router.get("/foundations/all", tags=["FoundationController"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "Example response with pictures": {
                        "value": foundation_list_example
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
async def foundations_get_select_all(
    is_need_pictures: bool = False,
    search_query: str | None = None,
    page: int | None = None,
    elements: int | None = None
):
    """Описание: получение данных обо всех фундаментах с поддержкой пагинации и поиска."""
    if page is not None and page < 1:
        raise HTTPException(status_code=400, detail="Ошибка: номер страницы должен быть положительным числом.")
    if elements is not None and elements < 1:
        raise HTTPException(status_code=400, detail="Ошибка: количество объектов на странице должно быть положительным числом.")

    conn = get_db_connection()
    x = get_foundations(conn, is_need_pictures, search_query, page, elements)
    return Response(
        json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"),
        status_code=200
    )


@router.get("/foundations/one", tags=["FoundationController"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "Example response with picture": {
                        "value": foundation_example
                    }
                }
            }
        }
    },
    404: {
        "description": "Foundation not found",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: фундамент с данным ID не найден."}
            }
        }
    }
})
async def foundations_get_one_foundation(foundation_id: int, is_need_pictures: bool = False):
    """Описание: получение данных об одном фундаменте по его идентификатору."""
    conn = get_db_connection()
    x = get_one_foundation(conn, foundation_id, is_need_pictures)
    if len(x) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: фундамент с данным ID не найден.")
    return Response(
        json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"),
        status_code=200
    )

@router.delete("/foundations/delete", tags=["FoundationController"], responses={
    200: {
        "description": "Foundation deleted successfully",
        "content": {
            "application/json": {
                "example": {"message": "Фундамент удалён."}
            }
        }
    },
    404: {
        "description": "Foundation not found",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: фундамент с данным ID не найден, потому удалить его невозможно."}
            }
        }
    }
})
async def foundations_delete(foundation_id: int,
    current_user: dict = Depends(get_current_active_admin_user)):
    """Описание: удаление фундамента по его ID."""
    conn = get_db_connection()
    y = get_one_foundation(conn, foundation_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: фундамент с данным ID не найден, потому удалить его невозможно.")
    x = delete_foundation(conn, foundation_id)
    return Response("{'message':'Фундамент удалён.'}", status_code=200)

@router.post("/foundations/insert", tags=["FoundationController"], responses={
    200: {
        "description": "Foundation created successfully",
        "content": {
            "application/json": {
                "example": {"message": "Фундамент создан."}
            }
        }
    },
    400: {
        "description": "Invalid input data",
        "content": {
            "application/json": {
                "examples": {
                    "Empty name": {
                        "value": {"detail": "Ошибка: название фундамента не должно быть пустым."}
                    },
                    "Name too long": {
                        "value": {"detail": "Ошибка: длина названия должна быть меньше или равна 30 символов."}
                    },
                    "Description too long": {
                        "value": {"detail": "Ошибка: длина описания должна быть меньше или равна 3000 символов."}
                    },
                    "Invalid depth": {
                        "value": {"detail": "Ошибка: глубина кровли коренного фундамента должна быть больше 0."}
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
async def foundations_insert(foundation_name: str, foundation_description: str | None = None, foundation_depth_roof_root_in_meters: float | None = None, foundation_picture_id: int | None = None,
    current_user: dict = Depends(get_current_active_admin_user)):
    """Описание: добавление фундамента. На ввод подаются название, описание, глубина кровли коренного фундамента и идентификатор картинки."""
    conn = get_db_connection()
    if foundation_name is not None and len(foundation_name) == 0:
        raise HTTPException(status_code=400, detail="Ошибка: название фундамента не должно быть пустым.")
    if foundation_name is not None and len(foundation_name) > 30:
        raise HTTPException(status_code=400, detail="Ошибка: длина названия должна быть меньше или равна 30 символов.")
    if foundation_description is not None and len(foundation_description) > 3000:
        raise HTTPException(status_code=400, detail="Ошибка: длина описания должна быть меньше или равна 3000 символов.")
    if foundation_depth_roof_root_in_meters is not None and foundation_depth_roof_root_in_meters < 0:
        raise HTTPException(status_code=400, detail="Ошибка: глубина кровли коренного фундамента должна быть больше 0.")
    if len(find_foundation_name(conn, foundation_name)) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: название должно быть уникальным (повторы не допускаются).")
    x = insert_foundation(conn, foundation_name, foundation_description, foundation_depth_roof_root_in_meters, foundation_picture_id)
    return JSONResponse(content = {'message' : 'Фундамент создан.'}, status_code=200)

@router.patch("/foundations/update", tags=["FoundationController"], responses={
    200: {
        "description": "Foundation updated successfully",
        "content": {
            "application/json": {
                "example": {"message": "Фундамент обновлён."}
            }
        }
    },
    400: {
        "description": "Invalid input data",
        "content": {
            "application/json": {
                "examples": {
                    "Empty name": {
                        "value": {"detail": "Ошибка: название фундамента не должно быть пустым."}
                    },
                    "Name too long": {
                        "value": {"detail": "Ошибка: длина названия должна быть меньше или равна 30 символов."}
                    },
                    "Description too long": {
                        "value": {"detail": "Ошибка: длина описания должна быть меньше или равна 3000 символов."}
                    },
                    "Invalid depth": {
                        "value": {"detail": "Ошибка: глубина кровли коренного фундамента должна быть больше 0."}
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
async def foundations_update(foundation_id: int, foundation_name: str | None = None, foundation_description: str | None = None, foundation_depth_roof_root_in_meters: float | None = None, foundation_picture_id: int | None = None,
    current_user: dict = Depends(get_current_active_admin_user)):
    """Описание: изменение параметров фундамента. На ввод подаются идентификатор, название, описание, глубина кровли коренного фундамента и идентификатор картинки."""
    conn = get_db_connection()
    if foundation_name is not None and len(foundation_name) == 0:
        raise HTTPException(status_code=400, detail="Ошибка: название фундамента не должно быть пустым.")
    if foundation_name is not None and len(foundation_name) > 30:
        raise HTTPException(status_code=400, detail="Ошибка: длина названия должна быть меньше или равна 30 символов.")
    if foundation_description is not None and len(foundation_description) > 3000:
        raise HTTPException(status_code=400, detail="Ошибка: длина описания должна быть меньше или равна 3000 символов.")
    if foundation_depth_roof_root_in_meters is not None and foundation_depth_roof_root_in_meters < 0:
        raise HTTPException(status_code=400, detail="Ошибка: глубина кровли коренного фундамента должна быть больше 0.")
    if len(find_foundation_name_with_id(conn, foundation_id, foundation_name)) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: название должно быть уникальным (повторы не допускаются).")
    x = update_foundation(conn, foundation_id, foundation_name, foundation_description, foundation_depth_roof_root_in_meters, foundation_picture_id)
    return JSONResponse(content = {'message' : 'Фундамент обновлён.'}, status_code=200)