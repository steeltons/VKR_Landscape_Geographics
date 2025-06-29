from fastapi import APIRouter, Response, HTTPException
import json
from models.picture_model import *
from utils import get_db_connection

router = APIRouter()

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
    }
})
async def pictures_get_select_all():
    """Описание: получение данных обо всех картинках."""
    conn = get_db_connection()
    x = get_pictures(conn)
    return Response(
        json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"),
        status_code=200
    )

@router.get("/pictures/one", tags=["PictureController"], responses={
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
async def pictures_get_one_picture(picture_id: int):
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
async def pictures_delete(picture_id: int):
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
    x = insert_picture(conn, picture_base64)
    return Response("{'message':'Картинка создана.'}", status_code=200)

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
async def pictures_update(picture_id: int, picture_base64: str):
    """Описание: изменение данных картинки. На ввод подаются идентификатор и строка в формате base64."""
    conn = get_db_connection()
    if len(picture_base64) == 0:
        raise HTTPException(status_code=400, detail="Ошибка: строка base64 не должна быть пустой.")
    x = update_picture(conn, picture_id, picture_base64)
    return Response("{'message':'Картинка обновлена.'}", status_code=200)
