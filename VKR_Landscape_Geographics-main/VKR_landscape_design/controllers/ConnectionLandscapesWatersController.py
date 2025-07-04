from fastapi import APIRouter, Response, HTTPException
import json
from models.connection_landscapes_waters_model import *
from utils import get_db_connection
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils import get_db_connection
from controllers.UserController import get_current_active_admin_user

router = APIRouter()
security = HTTPBearer()

connection_landscape_water_example = {
    "connection_id": 1,
    "landscape_id": 1,
    "water_id": 1
}

connection_landscape_water_list_example = [
    {
        "connection_id": 1,
        "landscape_id": 1,
        "water_id": 1
    },
    {
        "connection_id": 2,
        "landscape_id": 2,
        "water_id": 2
    }
]

@router.get("/connections_landscapes_waters/all", tags=["ConnectionLandscapesWatersController"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "Example response": {
                        "value": connection_landscape_water_list_example
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
async def connections_landscapes_waters_get_select_all(
    search_query: str | None = None,
    page: int | None = None,
    elements: int | None = None
):
    """Описание: получение данных обо всех связях ландшафтов и вод с поддержкой пагинации и поиска."""
    if page is not None and page < 1:
        raise HTTPException(status_code=400, detail="Ошибка: номер страницы должен быть положительным числом.")
    if elements is not None and elements < 1:
        raise HTTPException(status_code=400, detail="Ошибка: количество объектов на странице должно быть положительным числом.")

    conn = get_db_connection()
    x = get_connections_landscapes_waters(conn, search_query, page, elements)
    return Response(
        json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"),
        status_code=200
    )


@router.get("/connections_landscapes_waters/one", tags=["ConnectionLandscapesWatersController"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "Example response": {
                        "value": connection_landscape_water_example
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
async def connections_landscapes_waters_get_one_connection(connection_id: int):
    """Описание: получение данных об одной связи ландшафта и воды по её идентификатору."""
    conn = get_db_connection()
    x = get_one_connection_landscapes_waters(conn, connection_id)
    if len(x) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: связь с данным ID не найдена.")
    return Response(
        json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"),
        status_code=200
    )

@router.delete("/connections_landscapes_waters/delete", tags=["ConnectionLandscapesWatersController"], responses={
    200: {
        "description": "Connection deleted successfully",
        "content": {
            "application/json": {
                "example": {"message": "Связь ландшафта и воды удалена."}
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
async def connections_landscapes_waters_delete(connection_id: int,
    current_user: dict = Depends(get_current_active_admin_user)):
    """Описание: удаление связи ландшафта и воды по её ID."""
    conn = get_db_connection()
    y = get_one_connection_landscapes_waters(conn, connection_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: связь с данным ID не найдена, потому удалить её невозможно.")
    x = delete_connection_landscapes_waters(conn, connection_id)
    return Response("{'message':'Связь ландшафта и воды удалена.'}", status_code=200)

@router.post("/connections_landscapes_waters/insert", tags=["ConnectionLandscapesWatersController"], responses={
    200: {
        "description": "Connection created successfully",
        "content": {
            "application/json": {
                "example": {"message": "Связь ландшафта и воды создана."}
            }
        }
    }
})
async def connections_landscapes_waters_insert(landscape_id: int, water_id: int,
    current_user: dict = Depends(get_current_active_admin_user)):
    """Описание: добавление связи ландшафта и воды. На ввод подаются идентификаторы ландшафта и воды."""
    conn = get_db_connection()
    x = insert_connection_landscapes_waters(conn, landscape_id, water_id)
    return Response("{'message':'Связь ландшафта и воды создана.'}", status_code=200)

@router.patch("/connections_landscapes_waters/update", tags=["ConnectionLandscapesWatersController"], responses={
    200: {
        "description": "Connection updated successfully",
        "content": {
            "application/json": {
                "example": {"message": "Связь ландшафта и воды обновлена."}
            }
        }
    }
})
async def connections_landscapes_waters_update(connection_id: int, landscape_id: int, water_id: int,
    current_user: dict = Depends(get_current_active_admin_user)):
    """Описание: изменение параметров связи ландшафта и воды. На ввод подаются идентификатор связи, идентификаторы ландшафта и воды."""
    conn = get_db_connection()
    x = update_connection_landscapes_waters(conn, connection_id, landscape_id, water_id)
    return Response("{'message':'Связь ландшафта и воды обновлена.'}", status_code=200)
