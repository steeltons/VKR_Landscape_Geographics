from collections import defaultdict
from typing import Any

import pandas as pd
from sqlalchemy import create_engine

from app.configs.config import settings
from app.ml.features.feature_builder import FeatureBuilder
from app.ml.features.feature_schema import FEATURES


class DatasetBuilder:

    TASK_TYPES = [
        "agriculture",
        "construction",
        "ecology",
    ]

    def __init__(self) -> None:
        self.engine = create_engine(settings.training_database_url)
        self.feature_builder = FeatureBuilder()

    def build(self) -> pd.DataFrame:
        landscapes = self._load_landscapes()

        related = {
            "soils": self._load_related(
                connection_table="connections_landscapes_soils",
                target_table="soils",
                target_id_column="soil_id",
            ),
            "grounds": self._load_related(
                connection_table="connections_landscapes_grounds",
                target_table="grounds",
                target_id_column="ground_id",
            ),
            "plants": self._load_related(
                connection_table="connections_landscapes_plants",
                target_table="plants",
                target_id_column="plant_id",
            ),
            "reliefs": self._load_related(
                connection_table="connections_landscapes_reliefs",
                target_table="reliefs",
                target_id_column="relief_id",
            ),
            "foundations": self._load_related(
                connection_table="connections_landscapes_foundations",
                target_table="foundations",
                target_id_column="foundation_id",
            ),
            "waters": self._load_related(
                connection_table="connections_landscapes_waters",
                target_table="waters",
                target_id_column="water_id",
            ),
            "climates": self._load_related(
                connection_table="connections_landscapes_climates",
                target_table="climates",
                target_id_column="climate_id",
            ),
        }

        rows: list[dict[str, Any]] = []

        for landscape in landscapes:
            landscape_id = landscape["id"]

            raw_data = {
                "territory": {},
                "landscape": landscape,
                "soils": related["soils"].get(landscape_id, []),
                "grounds": related["grounds"].get(landscape_id, []),
                "plants": related["plants"].get(landscape_id, []),
                "reliefs": related["reliefs"].get(landscape_id, []),
                "foundations": related["foundations"].get(landscape_id, []),
                "waters": related["waters"].get(landscape_id, []),
                "climates": related["climates"].get(landscape_id, []),
            }

            for task_type in self.TASK_TYPES:
                features = self.feature_builder.build(
                    raw_data,
                    task_type=task_type,
                )

                rows.append(
                    {
                        "landscape_id": landscape_id,
                        "landscape_name": landscape.get("name"),
                        "task_type": task_type,
                        **{
                            feature_name: features.get(feature_name, 0.0)
                            for feature_name in FEATURES
                        },
                    }
                )

        return pd.DataFrame(rows)

    def _load_landscapes(self) -> list[dict[str, Any]]:
        query = """
            SELECT
                id,
                name,
                code,
                description,
                area_square,
                area_percentage,
                kr
            FROM landscapes
            WHERE is_active IS TRUE
            ORDER BY id
        """

        df = pd.read_sql(query, self.engine)
        return df.to_dict(orient="records")

    def _load_related(
        self,
        *,
        connection_table: str,
        target_table: str,
        target_id_column: str,
    ) -> dict[int, list[dict[str, Any]]]:
        query = f"""
            SELECT
                c.landscape_id,
                t.*
            FROM {connection_table} c
            JOIN {target_table} t
                ON t.id = c.{target_id_column}
            WHERE t.is_active IS TRUE
            ORDER BY c.landscape_id, t.id
        """

        df = pd.read_sql(query, self.engine)

        grouped: dict[int, list[dict[str, Any]]] = defaultdict(list)

        for row in df.to_dict(orient="records"):
            landscape_id = row.pop("landscape_id")
            grouped[landscape_id].append(row)

        return grouped