from fastapi import APIRouter, Response, HTTPException
import json
from models.landscapes_model import *
from utils import get_db_connection
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils import get_db_connection
from controllers.UserController import get_current_active_admin_user
from starlette.responses import JSONResponse

router = APIRouter()
security = HTTPBearer()

landscape_example = {
    "landscape_id": 1,
    "landscape_name": "Лес",
    "landscape_code": "FOR",
    "landscape_description": "Описание леса",
    "landscape_area_in_square_kilometers": 100.5,
    "landscape_area_in_percents": 10.5,
    "landscape_KR": 0.7,
    "landscape_picture_id": 1,
    "landscape_picture_base64": "base64_encoded_string_for_landscape"
}

landscape_list_example = [
    {
        "landscape_id": 1,
        "landscape_name": "Лес",
        "landscape_code": "FOR",
        "landscape_description": "Описание леса",
        "landscape_area_in_square_kilometers": 100.5,
        "landscape_area_in_percents": 10.5,
        "landscape_KR": 0.7,
        "landscape_picture_id": 1,
        "landscape_picture_base64": "base64_encoded_string_for_landscape"
    },
    {
        "landscape_id": 2,
        "landscape_name": "Пустыня",
        "landscape_code": "FOR",
        "landscape_description": "Описание пустыни",
        "landscape_area_in_square_kilometers": 100.5,
        "landscape_area_in_percents": 10.5,
        "landscape_KR": 0.7,
        "landscape_picture_id": 1,
        "landscape_picture_base64": "base64_encoded_string_for_landscape"
    }
]

@router.get("/landscapes/all", tags=["LandscapeController"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "Example response with pictures": {
                        "value": landscape_list_example
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
async def landscapes_get_select_all(
    is_need_pictures: bool = False,
    search_query: str | None = None,
    page: int | None = None,
    elements: int | None = None
):
    """Описание: получение данных обо всех ландшафтах с поддержкой пагинации и поиска."""
    if page is not None and page < 1:
        raise HTTPException(status_code=400, detail="Ошибка: номер страницы должен быть положительным числом.")
    if elements is not None and elements < 1:
        raise HTTPException(status_code=400, detail="Ошибка: количество объектов на странице должно быть положительным числом.")

    conn = get_db_connection()
    x = get_landscapes(conn, is_need_pictures, search_query, page, elements)
    return Response(
        json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"),
        status_code=200
    )


@router.get("/landscapes/one", tags=["LandscapeController"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "Example response with picture": {
                        "value": landscape_example
                    }
                }
            }
        }
    },
    404: {
        "description": "Landscape not found",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: ландшафт с данным ID не найден."}
            }
        }
    }
})
async def landscapes_get_one_landscape(landscape_id: int, is_need_pictures: bool = False):
    """Описание: получение данных об одном ландшафте по его идентификатору."""
    conn = get_db_connection()
    x = get_one_landscape(conn, landscape_id, is_need_pictures)
    if len(x) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: ландшафт с данным ID не найден.")
    return Response(
        json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"),
        status_code=200
    )

@router.delete("/landscapes/delete", tags=["LandscapeController"], responses={
    200: {
        "description": "Landscape deleted successfully",
        "content": {
            "application/json": {
                "example": {"message": "Ландшафт удалён."}
            }
        }
    },
    404: {
        "description": "Landscape not found",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: ландшафт с данным ID не найден, потому удалить его невозможно."}
            }
        }
    }
})
async def landscapes_delete(landscape_id: int,
    current_user: dict = Depends(get_current_active_admin_user)):
    """Описание: удаление ландшафта по его ID."""
    conn = get_db_connection()
    y = get_one_landscape(conn, landscape_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: ландшафт с данным ID не найден, потому удалить его невозможно.")
    x = delete_landscape(conn, landscape_id)
    return Response("{'message':'Ландшафт удалён.'}", status_code=200)

@router.post("/landscapes/insert", tags=["LandscapeController"], responses={
    200: {
        "description": "Landscape created successfully",
        "content": {
            "application/json": {
                "example": {"message": "Ландшафт создан."}
            }
        }
    },
    400: {
        "description": "Invalid input data",
        "content": {
            "application/json": {
                "examples": {
                    "Empty name": {
                        "value": {"detail": "Ошибка: название ландшафта не должно быть пустым."}
                    },
                    "Name too long": {
                        "value": {"detail": "Ошибка: длина названия должна быть меньше или равна 30 символов."}
                    },
                    "Code too long": {
                        "value": {"detail": "Ошибка: длина кода должна быть меньше или равна 30 символов."}
                    },
                    "Description too long": {
                        "value": {"detail": "Ошибка: длина описания должна быть меньше или равна 3000 символов."}
                    },
                    "Invalid area in square kilometers": {
                        "value": {"detail": "Ошибка: площадь в квадратных километрах должна быть больше 0."}
                    },
                    "Invalid area in percents": {
                        "value": {"detail": "Ошибка: площадь в процентах должна быть больше 0."}
                    },
                    "Invalid KR": {
                        "value": {"detail": "Ошибка: КР должна быть больше 0."}
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
async def landscapes_insert(landscape_name: str, landscape_code: str | None = None, landscape_description: str | None = None, landscape_area_in_square_kilometers: float | None = None, landscape_area_in_percents: float | None = None, landscape_KR: float | None = None, landscape_picture_id: int | None = None,
    current_user: dict = Depends(get_current_active_admin_user)):
    """Описание: добавление ландшафта. На ввод подаются название, код, описание, площадь в квадратных километрах, площадь в процентах, КР и идентификатор картинки."""
    conn = get_db_connection()
    if landscape_name is not None and len(landscape_name) == 0:
        raise HTTPException(status_code=400, detail="Ошибка: название ландшафта не должно быть пустым.")
    if landscape_name is not None and len(landscape_name) > 30:
        raise HTTPException(status_code=400, detail="Ошибка: длина названия должна быть меньше или равна 30 символов.")
    if landscape_code is not None and len(landscape_code) > 30:
        raise HTTPException(status_code=400, detail="Ошибка: длина кода должна быть меньше или равна 30 символов.")
    if landscape_description is not None and len(landscape_description) > 3000:
        raise HTTPException(status_code=400, detail="Ошибка: длина описания должна быть меньше или равна 3000 символов.")
    if landscape_area_in_square_kilometers is not None and landscape_area_in_square_kilometers < 0:
        raise HTTPException(status_code=400, detail="Ошибка: площадь в квадратных километрах должна быть больше 0.")
    if landscape_area_in_percents is not None and landscape_area_in_percents < 0:
        raise HTTPException(status_code=400, detail="Ошибка: площадь в процентах должна быть больше 0.")
    if landscape_KR is not None and landscape_KR < 0:
        raise HTTPException(status_code=400, detail="Ошибка: КР должна быть больше 0.")
    if len(find_landscape_name(conn, landscape_name)) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: название должно быть уникальным (повторы не допускаются).")
    x = insert_landscape(conn, landscape_name, landscape_code, landscape_description, landscape_area_in_square_kilometers, landscape_area_in_percents, landscape_KR, landscape_picture_id)
    return JSONResponse(content={'message': 'Ландшафт создан.'}, status_code=200)

@router.patch("/landscapes/update", tags=["LandscapeController"], responses={
    200: {
        "description": "Landscape updated successfully",
        "content": {
            "application/json": {
                "example": {"message": "Ландшафт обновлён."}
            }
        }
    },
    400: {
        "description": "Invalid input data",
        "content": {
            "application/json": {
                "examples": {
                    "Empty name": {
                        "value": {"detail": "Ошибка: название ландшафта не должно быть пустым."}
                    },
                    "Name too long": {
                        "value": {"detail": "Ошибка: длина названия должна быть меньше или равна 30 символов."}
                    },
                    "Code too long": {
                        "value": {"detail": "Ошибка: длина кода должна быть меньше или равна 30 символов."}
                    },
                    "Description too long": {
                        "value": {"detail": "Ошибка: длина описания должна быть меньше или равна 3000 символов."}
                    },
                    "Invalid area in square kilometers": {
                        "value": {"detail": "Ошибка: площадь в квадратных километрах должна быть больше 0."}
                    },
                    "Invalid area in percents": {
                        "value": {"detail": "Ошибка: площадь в процентах должна быть больше 0."}
                    },
                    "Invalid KR": {
                        "value": {"detail": "Ошибка: КР должна быть больше 0."}
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
async def landscapes_update(landscape_id: int, landscape_name: str | None = None, landscape_code: str | None = None, landscape_description: str | None = None, landscape_area_in_square_kilometers: float | None = None, landscape_area_in_percents: float | None = None, landscape_KR: float | None = None, landscape_picture_id: int | None = None,
    current_user: dict = Depends(get_current_active_admin_user)):
    """Описание: изменение параметров ландшафта. На ввод подаются идентификатор, название, код, описание, площадь в квадратных километрах, площадь в процентах, КР и идентификатор картинки."""
    conn = get_db_connection()
    if landscape_name is not None and len(landscape_name) == 0:
        raise HTTPException(status_code=400, detail="Ошибка: название ландшафта не должно быть пустым.")
    if landscape_name is not None and len(landscape_name) > 30:
        raise HTTPException(status_code=400, detail="Ошибка: длина названия должна быть меньше или равна 30 символов.")
    if landscape_code is not None and len(landscape_code) > 30:
        raise HTTPException(status_code=400, detail="Ошибка: длина кода должна быть меньше или равна 30 символов.")
    if landscape_description is not None and len(landscape_description) > 3000:
        raise HTTPException(status_code=400, detail="Ошибка: длина описания должна быть меньше или равна 3000 символов.")
    if landscape_area_in_square_kilometers is not None and landscape_area_in_square_kilometers < 0:
        raise HTTPException(status_code=400, detail="Ошибка: площадь в квадратных километрах должна быть больше 0.")
    if landscape_area_in_percents is not None and landscape_area_in_percents < 0:
        raise HTTPException(status_code=400, detail="Ошибка: площадь в процентах должна быть больше 0.")
    if landscape_KR is not None and landscape_KR < 0:
        raise HTTPException(status_code=400, detail="Ошибка: КР должна быть больше 0.")
    if len(find_landscape_name_with_id(conn, landscape_id, landscape_name)) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: название должно быть уникальным (повторы не допускаются).")
    x = update_landscape(conn, landscape_id, landscape_name, landscape_code, landscape_description, landscape_area_in_square_kilometers, landscape_area_in_percents, landscape_KR, landscape_picture_id)
    return JSONResponse(content={'message': 'Ландшафт обновлён.'}, status_code=200)
