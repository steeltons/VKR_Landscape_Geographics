from fastapi import APIRouter, Response, HTTPException
import json
from models.coords_model import *
from utils import get_db_connection
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils import get_db_connection
from controllers.UserController import get_current_active_admin_user

router = APIRouter()
security = HTTPBearer()

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
async def coords_get_select_all(
    search_query: str | None = None,
    page: int | None = None,
    elements: int | None = None
):
    """Описание: получение данных обо всех координатах с поддержкой пагинации и поиска."""
    if page is not None and page < 1:
        raise HTTPException(status_code=400, detail="Ошибка: номер страницы должен быть положительным числом.")
    if elements is not None and elements < 1:
        raise HTTPException(status_code=400, detail="Ошибка: количество объектов на странице должно быть положительным числом.")

    conn = get_db_connection()
    x = get_coords(conn, search_query, page, elements)
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
async def coords_delete(coord_id: int,
    current_user: dict = Depends(get_current_active_admin_user)):
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
    },
    400: {
        "description": "Invalid input parameters",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: недопустимые значения координат."}
            }
        }
    }
})
async def coords_insert(
    coord_x: float,
    coord_y: float,
    territorie_id: int,
    order: int,
    current_user: dict = Depends(get_current_active_admin_user)
):
    """Описание: добавление координаты. На ввод подаются координаты X, Y, идентификатор территории и порядок."""
    if (coord_x is not None) and ((coord_x < -90) or (coord_x > 90)):
        raise HTTPException(status_code=400, detail="Ошибка: координата X (широта) должна быть в интервале [-90; 90].")
    if (coord_y is not None) and ((coord_y <= -180) or (coord_y > 180)):
        raise HTTPException(status_code=400, detail="Ошибка: координата Y (долгота) должна быть в интервале (-180; 180].")

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
    },
    400: {
        "description": "Invalid input parameters",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: недопустимые значения координат."}
            }
        }
    }
})
async def coords_update(
    coord_id: int,
    coord_x: float | None = None,
    coord_y: float | None = None,
    territorie_id: int | None = None,
    order: int | None = None,
    current_user: dict = Depends(get_current_active_admin_user)
):
    """Описание: изменение параметров координаты. На ввод подаются идентификатор, координаты X, Y, идентификатор территории и порядок."""
    if (coord_x is not None) and ((coord_x < -90) or (coord_x > 90)):
        raise HTTPException(status_code=400, detail="Ошибка: координата X (широта) должна быть в интервале [-90; 90].")
    if (coord_y is not None) and ((coord_y <= -180) or (coord_y > 180)):
        raise HTTPException(status_code=400, detail="Ошибка: координата Y (долгота) должна быть в интервале (-180; 180].")

    conn = get_db_connection()
    x = update_coord(conn, coord_id, coord_x, coord_y, territorie_id, order)
    return Response("{'message':'Координата обновлена.'}", status_code=200)
