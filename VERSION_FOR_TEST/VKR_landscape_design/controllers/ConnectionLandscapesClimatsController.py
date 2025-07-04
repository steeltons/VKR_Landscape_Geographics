from fastapi import APIRouter, Response, HTTPException
import json
from models.connection_landscapes_climats_model import *
from utils import get_db_connection
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils import get_db_connection
from controllers.UserController import get_current_active_admin_user

router = APIRouter()
security = HTTPBearer()

connection_landscape_climat_example = {
    "connection_id": 1,
    "landscape_id": 1,
    "climat_id": 1
}

connection_landscape_climat_list_example = [
    {
        "connection_id": 1,
        "landscape_id": 1,
        "climat_id": 1
    },
    {
        "connection_id": 2,
        "landscape_id": 2,
        "climat_id": 2
    }
]

@router.get("/connections_landscapes_climats/all", tags=["ConnectionLandscapesClimatsController"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "Example response": {
                        "value": connection_landscape_climat_list_example
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
async def connections_landscapes_climats_get_select_all(
    search_query: str | None = None,
    page: int | None = None,
    elements: int | None = None
):
    """Описание: получение данных обо всех связях ландшафтов и климатов с поддержкой пагинации и поиска."""
    if page is not None and page < 1:
        raise HTTPException(status_code=400, detail="Ошибка: номер страницы должен быть положительным числом.")
    if elements is not None and elements < 1:
        raise HTTPException(status_code=400, detail="Ошибка: количество объектов на странице должно быть положительным числом.")

    conn = get_db_connection()
    x = get_connections_landscapes_climats(conn, search_query, page, elements)
    return Response(
        json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"),
        status_code=200
    )


@router.get("/connections_landscapes_climats/one", tags=["ConnectionLandscapesClimatsController"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "Example response": {
                        "value": connection_landscape_climat_example
                    }
                }
            }
        }
    },
    404: {
        "description": "Connection not found",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: связь с данным ID не найдена."}
            }
        }
    }
})
async def connections_landscapes_climats_get_one_connection(connection_id: int):
    """Описание: получение данных об одной связи ландшафта и климата по её идентификатору."""
    conn = get_db_connection()
    x = get_one_connection_landscapes_climats(conn, connection_id)
    if len(x) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: связь с данным ID не найдена.")
    return Response(
        json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"),
        status_code=200
    )

@router.delete("/connections_landscapes_climats/delete", tags=["ConnectionLandscapesClimatsController"], responses={
    200: {
        "description": "Connection deleted successfully",
        "content": {
            "application/json": {
                "example": {"message": "Связь ландшафта и климата удалена."}
            }
        }
    },
    404: {
        "description": "Connection not found",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: связь с данным ID не найдена, потому удалить её невозможно."}
            }
        }
    }
})
async def connections_landscapes_climats_delete(connection_id: int,
    current_user: dict = Depends(get_current_active_admin_user)):
    """Описание: удаление связи ландшафта и климата по её ID."""
    conn = get_db_connection()
    y = get_one_connection_landscapes_climats(conn, connection_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: связь с данным ID не найдена, потому удалить её невозможно.")
    x = delete_connection_landscapes_climats(conn, connection_id)
    return Response("{'message':'Связь ландшафта и климата удалена.'}", status_code=200)

@router.post("/connections_landscapes_climats/insert", tags=["ConnectionLandscapesClimatsController"], responses={
    200: {
        "description": "Connection created successfully",
        "content": {
            "application/json": {
                "example": {"message": "Связь ландшафта и климата создана."}
            }
        }
    }
})
async def connections_landscapes_climats_insert(landscape_id: int, climat_id: int,
    current_user: dict = Depends(get_current_active_admin_user)):
    """Описание: добавление связи ландшафта и климата. На ввод подаются идентификаторы ландшафта и климата."""
    conn = get_db_connection()
    x = insert_connection_landscapes_climats(conn, landscape_id, climat_id)
    return Response("{'message':'Связь ландшафта и климата создана.'}", status_code=200)

@router.patch("/connections_landscapes_climats/update", tags=["ConnectionLandscapesClimatsController"], responses={
    200: {
        "description": "Connection updated successfully",
        "content": {
            "application/json": {
                "example": {"message": "Связь ландшафта и климата обновлена."}
            }
        }
    }
})
async def connections_landscapes_climats_update(connection_id: int, landscape_id: int, climat_id: int,
    current_user: dict = Depends(get_current_active_admin_user)):
    """Описание: изменение параметров связи ландшафта и климата. На ввод подаются идентификатор связи, идентификаторы ландшафта и климата."""
    conn = get_db_connection()
    x = update_connection_landscapes_climats(conn, connection_id, landscape_id, climat_id)
    return Response("{'message':'Связь ландшафта и климата обновлена.'}", status_code=200)
