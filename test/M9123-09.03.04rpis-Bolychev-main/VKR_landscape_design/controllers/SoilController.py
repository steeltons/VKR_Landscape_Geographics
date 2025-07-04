from fastapi import APIRouter, Response, HTTPException
import json
from models.soils_model import *
from utils import get_db_connection
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils import get_db_connection
from controllers.UserController import get_current_active_admin_user

router = APIRouter()
security = HTTPBearer()

soil_example = {
    "soil_id": 1,
    "soil_name": "Чернозем",
    "soil_description": "Описание чернозема",
    "soil_acidity": 6.5,
    "soil_minerals": "Минералы чернозема",
    "soil_profile": "Профиль чернозема",
    "soil_picture_id": 1,
    "soil_picture_base64": "base64_encoded_string_for_soil"
}

soil_list_example = [
    {
        "soil_id": 1,
        "soil_name": "Чернозем",
        "soil_description": "Описание чернозема",
        "soil_acidity": 6.5,
        "soil_minerals": "Минералы чернозема",
        "soil_profile": "Профиль чернозема",
        "soil_picture_id": 1,
        "soil_picture_base64": "base64_encoded_string_for_soil"
    },
    {
        "soil_id": 2,
        "soil_name": "Подзол",
        "soil_description": "Описание подзола",
        "soil_acidity": 5.5,
        "soil_minerals": "Минералы подзола",
        "soil_profile": "Профиль подзола",
        "soil_picture_id": 2,
        "soil_picture_base64": "base64_encoded_string_for_soil"
    }
]

@router.get("/soils/all", tags=["SoilController"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "Example response with pictures": {
                        "value": soil_list_example
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
async def soils_get_select_all(
    is_need_pictures: bool = False,
    search_query: str | None = None,
    page: int | None = None,
    elements: int | None = None
):
    """Описание: получение данных обо всех почвах с поддержкой пагинации и поиска."""
    if page is not None and page < 1:
        raise HTTPException(status_code=400, detail="Ошибка: номер страницы должен быть положительным числом.")
    if elements is not None and elements < 1:
        raise HTTPException(status_code=400, detail="Ошибка: количество объектов на странице должно быть положительным числом.")

    conn = get_db_connection()
    x = get_soils(conn, is_need_pictures, search_query, page, elements)
    return Response(
        json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"),
        status_code=200
    )


@router.get("/soils/one", tags=["SoilController"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "Example response with picture": {
                        "value": soil_example
                    },
                    "Example response without picture": {
                        "value": soil_example
                    }
                }
            }
        }
    },
    404: {
        "description": "Soil not found",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: почва с данным ID не найдена."}
            }
        }
    }
})
async def soils_get_one_soil(soil_id: int, is_need_pictures: bool = False):
    """Описание: получение данных об одной почве по её идентификатору."""
    conn = get_db_connection()
    x = get_one_soil(conn, soil_id, is_need_pictures)
    if len(x) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: почва с данным ID не найдена.")
    return Response(
        json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"),
        status_code=200
    )

@router.delete("/soils/delete", tags=["SoilController"], responses={
    200: {
        "description": "Soil deleted successfully",
        "content": {
            "application/json": {
                "example": {"message": "Почва удалена."}
            }
        }
    },
    404: {
        "description": "Soil not found",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: почва с данным ID не найдена, потому удалить её невозможно."}
            }
        }
    }
})
async def soils_delete(soil_id: int,
    current_user: dict = Depends(get_current_active_admin_user)):
    """Описание: удаление почвы по её ID."""
    conn = get_db_connection()
    y = get_one_soil(conn, soil_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: почва с данным ID не найдена, потому удалить её невозможно.")
    x = delete_soil(conn, soil_id)
    return Response("{'message':'Почва удалена.'}", status_code=200)

@router.post("/soils/insert", tags=["SoilController"], responses={
    200: {
        "description": "Soil created successfully",
        "content": {
            "application/json": {
                "example": {"message": "Почва создана."}
            }
        }
    },
    400: {
        "description": "Invalid input data",
        "content": {
            "application/json": {
                "examples": {
                    "Empty name": {
                        "value": {"detail": "Ошибка: название почвы не должно быть пустым."}
                    },
                    "Name too long": {
                        "value": {"detail": "Ошибка: длина названия должна быть меньше или равна 30 символов."}
                    },
                    "Description too long": {
                        "value": {"detail": "Ошибка: длина описания должна быть меньше или равна 3000 символов."}
                    },
                    "Invalid acidity": {
                        "value": {"detail": "Ошибка: кислотность должна быть больше 0."}
                    },
                    "Minerals too long": {
                        "value": {"detail": "Ошибка: длина минералов должна быть меньше или равна 3000 символов."}
                    },
                    "Profile too long": {
                        "value": {"detail": "Ошибка: длина профиля должна быть меньше или равна 3000 символов."}
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
async def soils_insert(soil_name: str, soil_description: str | None = None, soil_acidity: float | None = None, soil_minerals: str | None = None, soil_profile: str | None = None, soil_picture_id: int | None = None,
    current_user: dict = Depends(get_current_active_admin_user)):
    """Описание: добавление почвы. На ввод подаются название, описание, кислотность, минералы, профиль и идентификатор картинки."""
    conn = get_db_connection()
    if soil_name is not None and len(soil_name) == 0:
        raise HTTPException(status_code=400, detail="Ошибка: название почвы не должно быть пустым.")
    if soil_name is not None and len(soil_name) > 30:
        raise HTTPException(status_code=400, detail="Ошибка: длина названия должна быть меньше или равна 30 символов.")
    if soil_description is not None and len(soil_description) > 3000:
        raise HTTPException(status_code=400, detail="Ошибка: длина описания должна быть меньше или равна 3000 символов.")
    if soil_acidity is not None and soil_acidity < 0:
        raise HTTPException(status_code=400, detail="Ошибка: кислотность должна быть больше 0.")
    if soil_minerals is not None and len(soil_minerals) > 3000:
        raise HTTPException(status_code=400, detail="Ошибка: длина минералов должна быть меньше или равна 3000 символов.")
    if soil_profile is not None and len(soil_profile) > 3000:
        raise HTTPException(status_code=400, detail="Ошибка: длина профиля должна быть меньше или равна 3000 символов.")
    if len(find_soil_name(conn, soil_name)) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: название должно быть уникальным (повторы не допускаются).")
    x = insert_soil(conn, soil_name, soil_description, soil_acidity, soil_minerals, soil_profile, soil_picture_id)
    return Response("{'message':'Почва создана.'}", status_code=200)

@router.patch("/soils/update", tags=["SoilController"], responses={
    200: {
        "description": "Soil updated successfully",
        "content": {
            "application/json": {
                "example": {"message": "Почва обновлена."}
            }
        }
    },
    400: {
        "description": "Invalid input data",
        "content": {
            "application/json": {
                "examples": {
                    "Empty name": {
                        "value": {"detail": "Ошибка: название почвы не должно быть пустым."}
                    },
                    "Name too long": {
                        "value": {"detail": "Ошибка: длина названия должна быть меньше или равна 30 символов."}
                    },
                    "Description too long": {
                        "value": {"detail": "Ошибка: длина описания должна быть меньше или равна 3000 символов."}
                    },
                    "Invalid acidity": {
                        "value": {"detail": "Ошибка: кислотность должна быть больше 0."}
                    },
                    "Minerals too long": {
                        "value": {"detail": "Ошибка: длина минералов должна быть меньше или равна 3000 символов."}
                    },
                    "Profile too long": {
                        "value": {"detail": "Ошибка: длина профиля должна быть меньше или равна 3000 символов."}
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
async def soils_update(soil_id: int, soil_name: str | None = None, soil_description: str | None = None, soil_acidity: float | None = None, soil_minerals: str | None = None, soil_profile: str | None = None, soil_picture_id: int | None = None,
    current_user: dict = Depends(get_current_active_admin_user)):
    """Описание: изменение параметров почвы. На ввод подаются идентификатор, название, описание, кислотность, минералы, профиль и идентификатор картинки."""
    conn = get_db_connection()
    if soil_name is not None and len(soil_name) == 0:
        raise HTTPException(status_code=400, detail="Ошибка: название почвы не должно быть пустым.")
    if soil_name is not None and len(soil_name) > 30:
        raise HTTPException(status_code=400, detail="Ошибка: длина названия должна быть меньше или равна 30 символов.")
    if soil_description is not None and len(soil_description) > 3000:
        raise HTTPException(status_code=400, detail="Ошибка: длина описания должна быть меньше или равна 3000 символов.")
    if soil_acidity is not None and soil_acidity < 0:
        raise HTTPException(status_code=400, detail="Ошибка: кислотность должна быть больше 0.")
    if soil_minerals is not None and len(soil_minerals) > 3000:
        raise HTTPException(status_code=400, detail="Ошибка: длина минералов должна быть меньше или равна 3000 символов.")
    if soil_profile is not None and len(soil_profile) > 3000:
        raise HTTPException(status_code=400, detail="Ошибка: длина профиля должна быть меньше или равна 3000 символов.")
    if len(find_soil_name_with_id(conn, soil_id, soil_name)) != 0:
        raise HTTPException(status_code=400, detail="Ошибка: название должно быть уникальным (повторы не допускаются).")
    x = update_soil(conn, soil_id, soil_name, soil_description, soil_acidity, soil_minerals, soil_profile, soil_picture_id)
    return Response("{'message':'Почва обновлена.'}", status_code=200)
