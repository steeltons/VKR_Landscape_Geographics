import hashlib
import json

from app.components.coordinates.coordinates_dc import (
    PolygonDC,
    PolygonPointDC,
    TerritoryCoordinatesDC,
    TerritoryCoordinatesItemDC,
)
from app.persistence.repositories.territory_geometry_repository import TerritoryGeometryRow


class CoordinatesComponentMapper:
    @staticmethod
    def to_dc(rows: list[TerritoryGeometryRow]) -> TerritoryCoordinatesDC:
        items: list[TerritoryCoordinatesItemDC] = []

        for row in rows:
            geojson = json.loads(row.geojson)

            polygons = [
                PolygonDC(
                    points=CoordinatesComponentMapper._polygon_to_points(
                        polygon_coordinates,
                    )
                )
                for polygon_coordinates in CoordinatesComponentMapper._extract_polygons(
                    geojson,
                )
            ]

            items.append(
                TerritoryCoordinatesItemDC(
                    territory_id=row.territory_id,
                    color=CoordinatesComponentMapper._build_color(row.territory_id),
                    polygons=polygons,
                )
            )

        return TerritoryCoordinatesDC(items=items)

    @staticmethod
    def _extract_polygons(geojson: dict) -> list[list[list[float]]]:
        geometry_type = geojson.get("type")
        coordinates = geojson.get("coordinates", [])

        if geometry_type == "Polygon":
            return [coordinates[0]]

        if geometry_type == "MultiPolygon":
            return [
                polygon[0]
                for polygon in coordinates
                if polygon and polygon[0]
            ]

        return []

    @staticmethod
    def _polygon_to_points(
        polygon_coordinates: list[list[float]],
    ) -> list[PolygonPointDC]:
        return [
            PolygonPointDC(
                longitude=float(coordinate[0]),
                latitude=float(coordinate[1]),
                order=index,
            )
            for index, coordinate in enumerate(polygon_coordinates)
        ]

    @staticmethod
    def _build_color(territory_id: int) -> str:
        digest = hashlib.md5(str(territory_id).encode("utf-8")).hexdigest()
        return f"#{digest[:6]}"