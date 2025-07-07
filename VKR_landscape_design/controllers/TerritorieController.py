from fastapi import APIRouter, Response, HTTPException, Depends
import json

from models.coords_model import delete_coord, delete_coord_by_territorie_id
from models.territories_model import *
from utils import get_db_connection
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from controllers.UserController import get_current_active_admin_user
from starlette.responses import JSONResponse

router = APIRouter()
security = HTTPBearer()

# Пример данных для ответов
territorie_example = {
    "territorie_id": 1,
    "territorie_landscape_id": 1,
    "territorie_description": "Описание территории",
    "territorie_color_r": 0,
    "territorie_color_g": 0,
    "territorie_color_b": 0
}

territorie_with_related_objects_example = {
    "territorie": {
        "territorie_id": 1,
        "territorie_landscape_id": 1,
        "territorie_description": "Описание территории",
        "territorie_color_r": 0,
        "territorie_color_g": 0,
        "territorie_color_b": 0
    },
    "landscape": {
        "landscape_id": 1,
        "landscape_name": "Ландшафт",
        "landscape_code": "LAND",
        "landscape_description": "Описание ландшафта",
        "landscape_area_in_square_kilometers": 100.0,
        "landscape_area_in_percents": 10.0,
        "landscape_KR": 0.5,
        "landscape_picture_id": 1,
        "landscape_picture_base64": "base64_encoded_string_for_landscape"
    },
    "soils": [
        {
            "soil_id": 1,
            "soil_name": "Почва",
            "soil_description": "Описание почвы",
            "soil_acidity": 7.0,
            "soil_minerals": "Минералы",
            "soil_profile": "Профиль",
            "soil_picture_id": 1,
            "soil_picture_base64": "base64_encoded_string_for_soil"
        }
    ],
    "grounds": [
        {
            "ground_id": 1,
            "ground_name": "Грунт",
            "ground_description": "Описание грунта",
            "ground_density": 1.5,
            "ground_humidity": 0.5,
            "ground_solidity": 0.8,
            "ground_picture_id": 1,
            "ground_picture_base64": "base64_encoded_string_for_ground"
        }
    ],
    "plants": [
        {
            "plant_id": 1,
            "plant_name": "Растение",
            "plant_description": "Описание растения",
            "plant_picture_id": 1,
            "plant_picture_base64": "base64_encoded_string_for_plant"
        }
    ],
    "reliefs": [
        {
            "relief_id": 1,
            "relief_name": "Рельеф",
            "relief_description": "Описание рельефа",
            "relief_picture_id": 1,
            "relief_picture_base64": "base64_encoded_string_for_relief"
        }
    ],
    "foundations": [
        {
            "foundation_id": 1,
            "foundation_name": "Фундамент",
            "foundation_description": "Описание фундамента",
            "foundation_depth_roof_root_in_meters": 2.0,
            "foundation_picture_id": 1,
            "foundation_picture_base64": "base64_encoded_string_for_foundation"
        }
    ],
    "waters": [
        {
            "water_id": 1,
            "water_name": "Вода",
            "water_description": "Описание воды",
            "water_picture_id": 1,
            "water_picture_base64": "base64_encoded_string_for_water"
        }
    ],
    "climats": [
        {
            "climat_id": 1,
            "climat_name": "Климат",
            "climat_description": "Описание климата",
            "climat_picture_id": 1,
            "climat_picture_base64": "base64_encoded_string_for_climat"
        }
    ]
}

territorie_list_example = [
    {
        "territorie_id": 1,
        "territorie_landscape_id": 1,
        "territorie_description": "Описание территории 1",
        "territorie_color_r": 0,
        "territorie_color_g": 0,
        "territorie_color_b": 0
    },
    {
        "territorie_id": 2,
        "territorie_landscape_id": 2,
        "territorie_description": "Описание территории 2",
        "territorie_color_r": 0,
        "territorie_color_g": 0,
        "territorie_color_b": 0
    }
]

coord_example = {
    "coord_id": 1,
    "coords_coord_x": 10.5,
    "coords_coord_y": 20.5,
    "coords_order": 1
}

coord_list_example = [
    {
        "coord_id": 1,
        "coords_coord_x": 10.5,
        "coords_coord_y": 20.5,
        "coords_order": 1
    },
    {
        "coord_id": 2,
        "coords_coord_x": 30.5,
        "coords_coord_y": 40.5,
        "coords_order": 2
    }
]

@router.get("/territories/all", tags=["TerritorieController"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "Example response": {
                        "value": territorie_list_example
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
async def territories_get_select_all(
    search_query: str | None = None,
    page: int | None = None,
    elements: int | None = None
):
    """Описание: получение данных обо всех территориях с поддержкой пагинации и поиска."""
    if page is not None and page < 1:
        raise HTTPException(status_code=400, detail="Ошибка: номер страницы должен быть положительным числом.")
    if elements is not None and elements < 1:
        raise HTTPException(status_code=400, detail="Ошибка: количество объектов на странице должно быть положительным числом.")

    conn = get_db_connection()
    x = get_territories(conn, search_query, page, elements)
    return Response(
        json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"),
        status_code=200
    )


@router.get("/territories/{territorie_id}/related-objects", tags=["TerritorieController"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "Example response": {
                        "value": territorie_with_related_objects_example
                    }
                }
            }
        }
    },
    404: {
        "description": "Territorie or related objects not found",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: территория или связанные объекты не найдены."}
            }
        }
    }
})
async def territories_get_related_objects(territorie_id: int, is_need_pictures: bool = False):
    """Описание: получение всех связанных объектов с территорией."""
    conn = get_db_connection()
    result = get_territorie_with_related_objects(conn, territorie_id, is_need_pictures)
    if result is None:
        raise HTTPException(status_code=404, detail="Ошибка: территория или связанные объекты не найдены.")
    return Response(
        json.dumps(result, indent=2, ensure_ascii=False),
        status_code=200
    )

@router.get("/territories/one", tags=["TerritorieController"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "Example response": {
                        "value": territorie_example
                    }
                }
            }
        }
    },
    404: {
        "description": "Territorie not found",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: территория с данным ID не найдена."}
            }
        }
    }
})
async def territories_get_one_territorie(territorie_id: int):
    """Описание: получение данных об одной территории по её идентификатору."""
    conn = get_db_connection()
    x = get_one_territorie(conn, territorie_id)
    if len(x) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: территория с данным ID не найдена.")
    return Response(
        json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"),
        status_code=200
    )

@router.get("/territories/{territorie_id}/coords", tags=["TerritorieController"], responses={
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
    404: {
        "description": "No coordinates found",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: координаты для данной территории не найдены."}
            }
        }
    }
})
async def territories_get_coords_by_territorie_id(territorie_id: int):
    """Описание: получение всех координат, связанных с определенной территорией."""
    conn = get_db_connection()
    x = get_coords_by_territorie_id(conn, territorie_id)
    if len(x) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: координаты для данной территории не найдены.")
    return Response(
        json.dumps(x.to_dict(orient="records"), indent=2, ensure_ascii=False).replace("NaN", "null"),
        status_code=200
    )

def get_all_territories(conn):
    # Получаем все территории из базы данных
    territories = pd.read_sql('SELECT territorie_id FROM territories', conn)
    return territories['territorie_id'].tolist()

@router.post("/territories/contains-point", tags=["TerritorieController"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "Point belongs to territories": {
                        "value": {"territorie_ids": [1, 2]}
                    },
                    "Point does not belong to any territory": {
                        "value": {"message": "Точка не принадлежит ни одной территории."}
                    }
                }
            }
        }
    }
})
async def check_point_in_territories(point_x: float, point_y: float):
    """Описание: Проверка принадлежности точки территориям.
    Принимает координаты точки и возвращает идентификаторы территорий, которым принадлежит точка."""
    conn = get_db_connection()
    territorie_ids = []
    territories = get_all_territories(conn)
    for territorie_id in territories:
        coords_df = get_coords_by_territorie_id(conn, territorie_id)
        if len(coords_df) == 0:
            continue
        polygon_coords = list(zip(coords_df['coords_coord_x'], coords_df['coords_coord_y']))
        is_inside = is_point_in_polygon(point_x, point_y, polygon_coords)
        if is_inside:
            territorie_ids.append(territorie_id)
    if not territorie_ids:
        return {"message": "Точка не принадлежит ни одной территории."}
    else:
        return {"territorie_ids": territorie_ids}

@router.post("/territories/{territorie_id}/contains-point", tags=["TerritorieController"], responses={
    200: {
        "description": "Point is inside the territory",
        "content": {
            "application/json": {
                "example": {"is_inside": True}
            }
        }
    },
    400: {
        "description": "Invalid input data",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: координаты точки не предоставлены."}
            }
        }
    },
    404: {
        "description": "No coordinates found",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: координаты для данной территории не найдены."}
            }
        }
    }
})
async def territories_contains_point(territorie_id: int, point_x: float, point_y: float):
    """Описание: проверка, находится ли точка внутри территории."""
    conn = get_db_connection()
    coords_df = get_coords_by_territorie_id(conn, territorie_id)
    if len(coords_df) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: координаты для данной территории не найдены.")
    polygon_coords = list(zip(coords_df['coords_coord_x'], coords_df['coords_coord_y']))
    is_inside = is_point_in_polygon(point_x, point_y, polygon_coords)
    return Response(
        json.dumps({"is_inside": is_inside}, indent=2),
        status_code=200
    )

@router.delete("/territories/delete", tags=["TerritorieController"], responses={
    200: {
        "description": "Territorie deleted successfully",
        "content": {
            "application/json": {
                "example": {"message": "Территория удалена."}
            }
        }
    },
    404: {
        "description": "Territorie not found",
        "content": {
            "application/json": {
                "example": {"detail": "Ошибка: территория с данным ID не найдена, потому удалить её невозможно."}
            }
        }
    }
})
async def territories_delete(territorie_id: int,
                             current_user: dict = Depends(get_current_active_admin_user)):
    """Описание: удаление территории по её ID."""
    conn = get_db_connection()
    y = get_one_territorie(conn, territorie_id)
    if len(y) == 0:
        raise HTTPException(status_code=404, detail="Ошибка: территория с данным ID не найдена, потому удалить её невозможно.")
    z = delete_coord_by_territorie_id(conn, territorie_id)
    x = delete_territorie(conn, territorie_id)
    return Response("{'message':'Территория удалена.'}", status_code=200)

@router.post("/territories/insert", tags=["TerritorieController"], responses={
    200: {
        "description": "Territorie created successfully",
        "content": {
            "application/json": {
                "example": {"message": "Территория создана."}
            }
        }
    }
})
async def territories_insert(
    territorie_landscape_id: int | None = None,
    territorie_description: str | None = None,
    territorie_color_r: int | None = None,
    territorie_color_g: int | None = None,
    territorie_color_b: int | None = None,
    current_user: dict = Depends(get_current_active_admin_user)
):
    """Описание: добавление территории. На ввод подаются идентификатор ландшафта и описание."""
    if (((territorie_color_r is not None) and ((territorie_color_r < 0) or (territorie_color_r > 255)))
            or ((territorie_color_g is not None) and ((territorie_color_g < 0) or (territorie_color_g > 255)))
            or ((territorie_color_b is not None) and ((territorie_color_b < 0) or (territorie_color_b > 255)))):
        raise HTTPException(status_code=400, detail="Ошибка: значения цветов должны быть в диапазоне от 0 до 255.")

    conn = get_db_connection()
    territorie_id = insert_territorie(
        conn,
        territorie_landscape_id,
        territorie_description,
        territorie_color_r,
        territorie_color_g,
        territorie_color_b
    )

    return JSONResponse(content={'message': 'Территория создана', 'id': territorie_id}, status_code=200)

@router.patch("/territories/update", tags=["TerritorieController"], responses={
    200: {
        "description": "Territorie updated successfully",
        "content": {
            "application/json": {
                "example": {"message": "Территория обновлена."}
            }
        }
    }
})
async def territories_update(
    territorie_id: int,
    territorie_landscape_id: int | None = None,
    territorie_description: str | None = None,
    territorie_color_r: int | None = None,
    territorie_color_g: int | None = None,
    territorie_color_b: int | None = None,
    current_user: dict = Depends(get_current_active_admin_user)
):
    """Описание: изменение параметров территории. На ввод подаются идентификатор, идентификатор ландшафта и описание."""

    if (((territorie_color_r is not None) and ((territorie_color_r < 0) or (territorie_color_r > 255)))
            or ((territorie_color_g is not None) and ((territorie_color_g < 0) or (territorie_color_g > 255)))
            or ((territorie_color_b is not None) and ((territorie_color_b < 0) or (territorie_color_b > 255)))):
        raise HTTPException(status_code=400, detail="Ошибка: значения цветов должны быть в диапазоне от 0 до 255.")

    conn = get_db_connection()
    y = get_one_territorie(conn, territorie_id)
    if len(y) == 0:
        raise HTTPException(status_code=404,
                            detail="Ошибка: территория с данным ID не найдена, потому обновить её невозможно.")
    x = update_territorie(conn, territorie_id, territorie_landscape_id, territorie_description, territorie_color_r, territorie_color_g, territorie_color_b)
    return Response("{'message':'Территория обновлена.'}", status_code=200)

@router.patch("/territories/untie_landscape", tags=["TerritorieController"], responses={
    200: {
        "description": "Territorie untie landscape successfully",
        "content": {
            "application/json": {
                "example": {"message": "Ландшафт отвязан от территории."}
            }
        }
    }
})
async def territories_untie_landscape(
    territorie_id: int,
    current_user: dict = Depends(get_current_active_admin_user)
):
    """Описание: отвязка ландшафта от территории. На вход подаётся идентификатор территории, от которой нужно отвязать ландшафт."""
    conn = get_db_connection()
    y = get_one_territorie(conn, territorie_id)
    if len(y) == 0:
        raise HTTPException(status_code=404,
                            detail="Ошибка: территория с данным ID не найдена, потому отвязать ландшафт от неё невозможно.")
    x = untie_landscape_from_territorie(conn, territorie_id)
    return Response("{'message':'Ландшафт отвязан от территории.'}", status_code=200)

@router.post("/territories/point-related-objects", tags=["TerritorieController"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "Example response": {
                        "value": {
                            "territories": [
                                {
                                    "territorie": territorie_example,
                                    "landscape": territorie_with_related_objects_example["landscape"],
                                    "soils": territorie_with_related_objects_example["soils"],
                                    "grounds": territorie_with_related_objects_example["grounds"],
                                    "plants": territorie_with_related_objects_example["plants"],
                                    "reliefs": territorie_with_related_objects_example["reliefs"],
                                    "foundations": territorie_with_related_objects_example["foundations"],
                                    "waters": territorie_with_related_objects_example["waters"],
                                    "climats": territorie_with_related_objects_example["climats"]
                                }
                            ]
                        }
                    },
                    "Point does not belong to any territory": {
                        "value": {"message": "Точка не принадлежит ни одной территории."}
                    }
                }
            }
        }
    }
})
async def get_related_objects_for_point(point_x: float, point_y: float, is_need_pictures: bool = False):
    """Описание: Получение всех связанных объектов для территорий, которым принадлежит точка.
    Принимает координаты точки и флаг is_need_pictures."""
    conn = get_db_connection()
    territorie_ids = []
    territories = get_all_territories(conn)
    for territorie_id in territories:
        coords_df = get_coords_by_territorie_id(conn, territorie_id)
        if len(coords_df) == 0:
            continue
        polygon_coords = list(zip(coords_df['coords_coord_x'], coords_df['coords_coord_y']))
        is_inside = is_point_in_polygon(point_x, point_y, polygon_coords)
        if is_inside:
            territorie_ids.append(territorie_id)
    if not territorie_ids:
        raise HTTPException(status_code=404, detail="Точка не принадлежит ни одной территории.")
    result = []
    for territorie_id in territorie_ids:
        territorie_data = get_territorie_with_related_objects(conn, territorie_id, is_need_pictures)
        if territorie_data:
            result.append(territorie_data)
    return Response(
        json.dumps({"territories": result}, indent=2, ensure_ascii=False),
        status_code=200
    )