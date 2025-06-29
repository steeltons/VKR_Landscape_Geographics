from fastapi import APIRouter, Response, HTTPException
import json
from models.coords_model import *
from utils import get_db_connection

router = APIRouter()

coord_example = {
    "coord_id": 1,
    "coords_coord_x": 10.5,
    "coords_coord_y": 20.5,
    "coords_territorie_id": 1,
    "coords_order": 1
}

coord_list_example = [
    {
        "coord_id": 1,
        "coords_coord_x": 10.5,
        "coords_coord_y": 20.5,
        "coords_territorie_id": 1,
        "coords_order": 1
    },
    {
        "coord_id": 2,
        "coords_coord_x": 30.5,
        "coords_coord_y": 40.5,
        "coords_territorie_id": 2,
        "coords_order": 2
    }
]

@router.get("/coords/all", tags=["CoordController"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "Example response": {
                        "value": coord_list_example
                    }
                }
            }
        }
    }
})
async def coords_get_select_all():
    """Описание: получение данных обо всех координатах."""
    conn = get_db_connection()
    x = get_coords(conn)
    return Response(
        json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"),
        status_code=200
    )

@router.get("/coords/one", tags=["CoordController"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "Example response": {
                        "value": coord_example
                    }
                }
            }
        }
    },
    404: {
        "description": "Coord not found",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: координата с данным ID не найдена."}
            }
        }
    }
})
async def coords_get_one_coord(coord_id: int):
    """Описание: получение данных об одной координате по её идентификатору."""
    conn = get_db_connection()
    x = get_one_coord(conn, coord_id)
    if len(x) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: координата с данным ID не найдена.")
    return Response(
        json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"),
        status_code=200
    )

@router.delete("/coords/delete", tags=["CoordController"], responses={
    200: {
        "description": "Coord deleted successfully",
        "content": {
            "application/json": {
                "example": {"message": "Координата удалена."}
            }
        }
    },
    404: {
        "description": "Coord not found",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: координата с данным ID не найдена, потому удалить её невозможно."}
            }
        }
    }
})
async def coords_delete(coord_id: int):
    """Описание: удаление координаты по её ID."""
    conn = get_db_connection()
    y = get_one_coord(conn, coord_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: координата с данным ID не найдена, потому удалить её невозможно.")
    x = delete_coord(conn, coord_id)
    return Response("{'message':'Координата удалена.'}", status_code=200)

@router.post("/coords/insert", tags=["CoordController"], responses={
    200: {
        "description": "Coord created successfully",
        "content": {
            "application/json": {
                "example": {"message": "Координата создана."}
            }
        }
    }
})
async def coords_insert(coord_x: float, coord_y: float, territorie_id: int, order: int):
    """Описание: добавление координаты. На ввод подаются координаты X, Y, идентификатор территории и порядок."""
    conn = get_db_connection()
    x = insert_coord(conn, coord_x, coord_y, territorie_id, order)
    return Response("{'message':'Координата создана.'}", status_code=200)

@router.patch("/coords/update", tags=["CoordController"], responses={
    200: {
        "description": "Coord updated successfully",
        "content": {
            "application/json": {
                "example": {"message": "Координата обновлена."}
            }
        }
    }
})
async def coords_update(coord_id: int, coord_x: float, coord_y: float, territorie_id: int, order: int):
    """Описание: изменение параметров координаты. На ввод подаются идентификатор, координаты X, Y, идентификатор территории и порядок."""
    conn = get_db_connection()
    x = update_coord(conn, coord_id, coord_x, coord_y, territorie_id, order)
    return Response("{'message':'Координата обновлена.'}", status_code=200)
