from controllers.UserController import get_current_active_admin_user
from models.climats_model import *
from fastapi import APIRouter, Response, HTTPException
import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils import get_db_connection

router = APIRouter()
security = HTTPBearer()

# Пример данных для ответов
climat_example = {
    "climat_id": 1,
    "climat_name": "Умеренный",
    "climat_description": "Описание умеренного климата",
    "climat_picture_id": 1,
    "climat_picture_base64": "base64_encoded_string_for_climat"
}

climat_list_example = [
    {
        "climat_id": 1,
        "climat_name": "Умеренный",
        "climat_description": "Описание умеренного климата",
        "climat_picture_id": 1,
        "climat_picture_base64": "base64_encoded_string_for_climat"
    },
    {
        "climat_id": 2,
        "climat_name": "Тропический",
        "climat_description": "Описание тропического климата",
        "climat_picture_id": 2,
        "climat_picture_base64": "base64_encoded_string_for_climat"
    }
]

@router.get("/climats/all", tags=["ClimatController"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "Example response with pictures": {
                        "value": climat_list_example
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
async def climats_get_select_all(
    is_need_pictures: bool = False,
    search_query: str | None = None,
    page: int | None = None,
    elements: int | None = None
):
    """Описание: получение данных обо всех климатах с поддержкой пагинации и поиска."""
    if page is not None and page < 1:
        raise HTTPException(status_code=400, detail="Ошибка: номер страницы должен быть положительным числом.")
    if elements is not None and elements < 1:
        raise HTTPException(status_code=400, detail="Ошибка: количество объектов на странице должно быть положительным числом.")

    conn = get_db_connection()
    x = get_climats(conn, is_need_pictures, search_query, page, elements)
    return Response(
        json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"),
        status_code=200
    )


@router.get("/climats/one", tags=["ClimatController"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "Example response with picture": {
                        "value": climat_example
                    }
                }
            }
        }
    },
    404: {
        "description": "Climat not found",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: климат с данным ID не найден."}
            }
        }
    }
})
async def climats_get_one_climat(climat_id: int, is_need_pictures: bool = False):
    """Описание: получение данных об одном климате по его идентификатору."""
    conn = get_db_connection()
    x = get_one_climat(conn, climat_id, is_need_pictures)
    if len(x) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: климат с данным ID не найден.")
    return Response(
        json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"),
        status_code=200
    )

@router.delete("/climats/delete", tags=["ClimatController"], responses={
    200: {
        "description": "Climat deleted successfully",
        "content": {
            "application/json": {
                "example": {"message": "Климат удалён."}
            }
        }
    },
    404: {
        "description": "Climat not found",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: климат с данным ID не найден, потому удалить его невозможно."}
            }
        }
    },
    403: {
        "description": "Forbidden",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: у пользователя недостаточно прав для выполнения этой операции."}
            }
        }
    }
})
async def climats_delete(climat_id: int, current_user: dict = Depends(get_current_active_admin_user)):
    """Описание: удаление климата по его ID."""
    conn = get_db_connection()
    y = get_one_climat(conn, climat_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: климат с данным ID не найден, потому удалить его невозможно.")
    x = delete_climat(conn, climat_id)
    return Response("{'message':'Климат удалён.'}", status_code=200)

@router.post("/climats/insert", tags=["ClimatController"], responses={
    200: {
        "description": "Climat created successfully",
        "content": {
            "application/json": {
                "example": {"message": "Климат создан."}
            }
        }
    },
    400: {
        "description": "Invalid input data",
        "content": {
            "application/json": {
                "examples": {
                    "Empty name": {
                        "value": {"detail": "Ошибка: название климата не должно быть пустым."}
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
async def climats_insert(climat_name: str, climat_description: str | None = None, climat_picture_id: int | None = None,
    current_user: dict = Depends(get_current_active_admin_user)):
    """Описание: добавление климата. На ввод подаются название, описание и идентификатор картинки."""
    conn = get_db_connection()
    if climat_name is not None and len(climat_name) == 0:
        raise HTTPException(status_code=400, detail="Ошибка: название климата не должно быть пустым.")
    if climat_name is not None and len(climat_name) > 30:
        raise HTTPException(status_code=400, detail="Ошибка: длина названия должна быть меньше или равна 30 символов.")
    if climat_description is not None and len(climat_description) > 3000:
        raise HTTPException(status_code=400, detail="Ошибка: длина описания должна быть меньше или равна 3000 символов.")
    if len(find_climat_name(conn, climat_name)) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: название должно быть уникальным (повторы не допускаются).")
    x = insert_climat(conn, climat_name, climat_description, climat_picture_id)
    return Response("{'message':'Климат создан.'}", status_code=200)

@router.patch("/climats/update", tags=["ClimatController"], responses={
    200: {
        "description": "Climat updated successfully",
        "content": {
            "application/json": {
                "example": {"message": "Климат обновлён."}
            }
        }
    },
    400: {
        "description": "Invalid input data",
        "content": {
            "application/json": {
                "examples": {
                    "Empty name": {
                        "value": {"detail": "Ошибка: название климата не должно быть пустым."}
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
async def climats_update(climat_id: int, climat_name: str | None = None, climat_description: str | None = None, climat_picture_id: int | None = None,
    current_user: dict = Depends(get_current_active_admin_user)):
    """Описание: изменение параметров климата. На ввод подаются идентификатор, название, описание и идентификатор картинки."""
    conn = get_db_connection()
    if climat_id is not None and climat_id < 0:
        raise HTTPException(status_code=400, detail="Ошибка: идентификатор климата должен быть больше 0.")
    if climat_name is not None and len(climat_name) == 0:
        raise HTTPException(status_code=400, detail="Ошибка: название климата не должно быть пустым.")
    if climat_name is not None and len(climat_name) > 30:
        raise HTTPException(status_code=400, detail="Ошибка: длина названия должна быть меньше или равна 30 символов.")
    if climat_description is not None and len(climat_description) > 3000:
        raise HTTPException(status_code=400, detail="Ошибка: длина описания должна быть меньше или равна 3000 символов.")
    if len(find_climat_name_with_id(conn, climat_id, climat_name)) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: название должно быть уникальным (повторы не допускаются).")
    x = update_climat(conn, climat_id, climat_name, climat_description, climat_picture_id)
    return Response("{'message':'Климат обновлён.'}", status_code=200)
