from fastapi import APIRouter, Response, HTTPException
import json
from models.connection_landscapes_foundations_model import *
from utils import get_db_connection

router = APIRouter()

connection_landscape_foundation_example = {
    "connection_id": 1,
    "landscape_id": 1,
    "foundation_id": 1
}

connection_landscape_foundation_list_example = [
    {
        "connection_id": 1,
        "landscape_id": 1,
        "foundation_id": 1
    },
    {
        "connection_id": 2,
        "landscape_id": 2,
        "foundation_id": 2
    }
]

@router.get("/connections_landscapes_foundations/all", tags=["ConnectionLandscapesFoundationsController"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "Example response": {
                        "value": connection_landscape_foundation_list_example
                    }
                }
            }
        }
    }
})
async def connections_landscapes_foundations_get_select_all():
    """Описание: получение данных обо всех связях ландшафтов и фундаментов."""
    conn = get_db_connection()
    x = get_connections_landscapes_foundations(conn)
    return Response(
        json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"),
        status_code=200
    )

@router.get("/connections_landscapes_foundations/one", tags=["ConnectionLandscapesFoundationsController"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "Example response": {
                        "value": connection_landscape_foundation_example
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
async def connections_landscapes_foundations_get_one_connection(connection_id: int):
    """Описание: получение данных об одной связи ландшафта и фундамента по её идентификатору."""
    conn = get_db_connection()
    x = get_one_connection_landscapes_foundations(conn, connection_id)
    if len(x) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: связь с данным ID не найдена.")
    return Response(
        json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"),
        status_code=200
    )

@router.delete("/connections_landscapes_foundations/delete", tags=["ConnectionLandscapesFoundationsController"], responses={
    200: {
        "description": "Connection deleted successfully",
        "content": {
            "application/json": {
                "example": {"message": "Связь ландшафта и фундамента удалена."}
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
async def connections_landscapes_foundations_delete(connection_id: int):
    """Описание: удаление связи ландшафта и фундамента по её ID."""
    conn = get_db_connection()
    y = get_one_connection_landscapes_foundations(conn, connection_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: связь с данным ID не найдена, потому удалить её невозможно.")
    x = delete_connection_landscapes_foundations(conn, connection_id)
    return Response("{'message':'Связь ландшафта и фундамента удалена.'}", status_code=200)

@router.post("/connections_landscapes_foundations/insert", tags=["ConnectionLandscapesFoundationsController"], responses={
    200: {
        "description": "Connection created successfully",
        "content": {
            "application/json": {
                "example": {"message": "Связь ландшафта и фундамента создана."}
            }
        }
    }
})
async def connections_landscapes_foundations_insert(landscape_id: int, foundation_id: int):
    """Описание: добавление связи ландшафта и фундамента. На ввод подаются идентификаторы ландшафта и фундамента."""
    conn = get_db_connection()
    x = insert_connection_landscapes_foundations(conn, landscape_id, foundation_id)
    return Response("{'message':'Связь ландшафта и фундамента создана.'}", status_code=200)

@router.patch("/connections_landscapes_foundations/update", tags=["ConnectionLandscapesFoundationsController"], responses={
    200: {
        "description": "Connection updated successfully",
        "content": {
            "application/json": {
                "example": {"message": "Связь ландшафта и фундамента обновлена."}
            }
        }
    }
})
async def connections_landscapes_foundations_update(connection_id: int, landscape_id: int, foundation_id: int):
    """Описание: изменение параметров связи ландшафта и фундамента. На ввод подаются идентификатор связи, идентификаторы ландшафта и фундамента."""
    conn = get_db_connection()
    x = update_connection_landscapes_foundations(conn, connection_id, landscape_id, foundation_id)
    return Response("{'message':'Связь ландшафта и фундамента обновлена.'}", status_code=200)
