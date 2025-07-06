from fastapi import APIRouter, Response, HTTPException
import json
from models.picture_model import *
from fastapi import UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
import base64
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils import get_db_connection
from controllers.UserController import get_current_user, get_current_active_admin_user
from fastapi import Path

router = APIRouter()
security = HTTPBearer()

picture_example = {
    "picture_id": 1,
    "picture_base64": "base64encodedstring"
}

picture_list_example = [
    {
        "picture_id": 1,
        "picture_base64": "base64encodedstring1"
    },
    {
        "picture_id": 2,
        "picture_base64": "base64encodedstring2"
    }
]

@router.get("/pictures/all", tags=["PictureController"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "Example response": {
                        "value": picture_list_example
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
async def pictures_get_select_all(
    search_query: str | None = None,
    page: int | None = None,
    elements: int | None = None
):
    """Описание: получение данных обо всех картинках с поддержкой пагинации и поиска."""
    if page is not None and page < 1:
        raise HTTPException(status_code=400, detail="Ошибка: номер страницы должен быть положительным числом.")
    if elements is not None and elements < 1:
        raise HTTPException(status_code=400, detail="Ошибка: количество объектов на странице должно быть положительным числом.")

    conn = get_db_connection()
    x = get_pictures(conn, search_query, page, elements)
    return Response(
        json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"),
        status_code=200
    )




@router.get("/pictures/{picture_id}", tags=["PictureController"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "Example response": {
                        "value": picture_example
                    }
                }
            }
        }
    },
    404: {
        "description": "Picture not found",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: картинка с данным ID не найдена."}
            }
        }
    }
})
async def pictures_get_one_picture(picture_id: int = Path(..., description="ID картинки")):
    """Описание: получение данных об одной картинке по её идентификатору."""
    conn = get_db_connection()
    x = get_one_picture(conn, picture_id)
    if len(x) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: картинка с данным ID не найдена.")
    return Response(
        json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"),
        status_code=200
    )

@router.delete("/pictures/delete", tags=["PictureController"], responses={
    200: {
        "description": "Picture deleted successfully",
        "content": {
            "application/json": {
                "example": {"message": "Картинка удалена."}
            }
        }
    },
    404: {
        "description": "Picture not found",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: картинка с данным ID не найдена, потому удалить её невозможно."}
            }
        }
    }
})
async def pictures_delete(picture_id: int,
    current_user: dict = Depends(get_current_active_admin_user)):
    """Описание: удаление картинки по её ID."""
    conn = get_db_connection()
    y = get_one_picture(conn, picture_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: картинка с данным ID не найдена, потому удалить её невозможно.")
    x = delete_picture(conn, picture_id)
    return Response("{'message':'Картинка удалена.'}", status_code=200)

@router.post("/pictures/insert", tags=["PictureController"], responses={
    200: {
        "description": "Picture created successfully",
        "content": {
            "application/json": {
                "example": {"message": "Картинка создана."}
            }
        }
    },
    400: {
        "description": "Invalid input data",
        "content": {
            "application/json": {
                "examples": {
                    "Empty base64": {
                        "value": {"detail": "Ошибка: строка base64 не должна быть пустой."}
                    }
                }
            }
        }
    }
})
async def pictures_insert(picture_base64: str):
    """Описание: добавление картинки. На ввод подаётся строка в формате base64."""
    conn = get_db_connection()
    if len(picture_base64) == 0:
        raise HTTPException(status_code=400, detail="Ошибка: строка base64 не должна быть пустой.")
    if len(picture_base64) > 1500000:
        raise HTTPException(status_code=400, detail="Ошибка: строка base64 не должна превышать 1500000 символов.")
    x = insert_picture(conn, picture_base64)
    return Response("{'message':'Картинка создана.'}", status_code=200)

@router.post("/pictures", tags=["PictureController"], responses={
    200: {
        "description": "Picture uploaded successfully",
        "content": {
            "application/json": {
                "example": {"id": 1, "message": "Картинка создана."}
            }
        }
    },
    400: {
        "description": "Invalid input data",
        "content": {
            "application/json": {
                "examples": {
                    "No file": {
                        "value": {"detail": "Файл изображения не был передан."}
                    }
                }
            }
        }
    }
})
async def pictures_insert(file: UploadFile = File(...)):
    """Добавление картинки. Принимает файл изображения и сохраняет в базу."""
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Файл изображения не был передан.")

    base64_image = base64.b64encode(content).decode("utf-8")

    conn = get_db_connection()
    pic_id = insert_picture(conn, base64_image)

    return JSONResponse(status_code=200, content={"id": pic_id, "message": "Картинка создана."})

@router.patch("/pictures/update", tags=["PictureController"], responses={
    200: {
        "description": "Picture updated successfully",
        "content": {
            "application/json": {
                "example": {"message": "Картинка обновлена."}
            }
        }
    },
    400: {
        "description": "Invalid input data",
        "content": {
            "application/json": {
                "examples": {
                    "Empty base64": {
                        "value": {"detail": "Ошибка: строка base64 не должна быть пустой."}
                    }
                }
            }
        }
    }
})
async def pictures_update(picture_id: int, picture_base64: str,
    current_user: dict = Depends(get_current_active_admin_user)):
    """Описание: изменение данных картинки. На ввод подаются идентификатор и строка в формате base64."""
    conn = get_db_connection()
    if len(picture_base64) == 0:
        raise HTTPException(status_code=400, detail="Ошибка: строка base64 не должна быть пустой.")
    x = update_picture(conn, picture_id, picture_base64)
    return Response("{'message':'Картинка обновлена.'}", status_code=200)
