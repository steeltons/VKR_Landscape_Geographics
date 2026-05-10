from statistics import mean
from typing import Any

from app.ml.features.feature_schema import FEATURES


class FeatureBuilder:

    def _to_float(self, value: Any, default: float = 0.0) -> float:
        if value is None:
            return default

        try:
            return float(str(value).replace(",", "."))
        except (ValueError, TypeError):
            return default

    def _to_int(self, value: Any, default: int = 0) -> int:
        if value is None:
            return default

        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    def _safe_mean(self, values: list[float]) -> float:
        return mean(values) if values else 0.0

    def _has_value(self, value: Any) -> int:
        return 1 if value not in (None, "", []) else 0

    def build(self, data: dict, task_type: str | None = None) -> dict[str, float]:
        features: dict[str, float | int] = {}

        soils = data.get("soils") or []

        acidity_values = [
            self._to_float(soil.get("acidity"))
            for soil in soils
            if soil.get("acidity") is not None
        ]

        features["soil_acidity_mean"] = self._safe_mean(acidity_values)
        features["soil_count"] = len(soils)
        features["soil_has_minerals"] = max(
            [self._has_value(soil.get("minerals")) for soil in soils],
            default=0,
        )

        grounds = data.get("grounds") or []

        density_values = [
            self._to_float(ground.get("density"))
            for ground in grounds
            if ground.get("density") is not None
        ]

        humidity_values = [
            self._to_float(ground.get("humidity"))
            for ground in grounds
            if ground.get("humidity") is not None
        ]

        solidity_values = [
            self._to_float(ground.get("solidity"))
            for ground in grounds
            if ground.get("solidity") is not None
        ]

        features["ground_density_mean"] = self._safe_mean(density_values)
        features["ground_humidity_mean"] = self._safe_mean(humidity_values)
        features["ground_solidity_mean"] = self._safe_mean(solidity_values)
        features["ground_count"] = len(grounds)

        climates = data.get("climates") or []

        features["climate_count"] = len(climates)
        features["has_climate"] = 1 if climates else 0

        reliefs = data.get("reliefs") or []

        features["relief_count"] = len(reliefs)
        features["has_relief"] = 1 if reliefs else 0

        plants = data.get("plants") or []

        features["plant_count"] = len(plants)
        features["has_plants"] = 1 if plants else 0

        waters = data.get("waters") or []

        features["water_count"] = len(waters)
        features["has_water"] = 1 if waters else 0

        foundations = data.get("foundations") or []

        roof_root_depth_values = [
            self._to_float(foundation.get("roof_root_depth"))
            for foundation in foundations
            if foundation.get("roof_root_depth") is not None
        ]

        features["foundation_count"] = len(foundations)
        features["foundation_roof_root_depth_mean"] = self._safe_mean(
            roof_root_depth_values,
        )
        features["has_foundation"] = 1 if foundations else 0

        landscape = data.get("landscape") or {}

        features["landscape_kr"] = self._to_float(
            landscape.get("kr"),
        )
        features["has_landscape"] = 1 if landscape else 0

        territory = data.get("territory") or {}

        features["has_territory"] = 1 if territory else 0

        task_type = (task_type or "").lower().strip()

        features["task_agriculture"] = 1 if task_type == "agriculture" else 0
        features["task_construction"] = 1 if task_type == "construction" else 0
        features["task_ecology"] = 1 if task_type == "ecology" else 0

        features = self._normalize(features)
        features = self._ensure_all_features(features)

        return features

    def _normalize(self, features: dict[str, float | int]) -> dict[str, float]:
        normalized: dict[str, float] = {}

        for key, value in features.items():
            if isinstance(value, bool):
                normalized[key] = 1.0 if value else 0.0
                continue

            if isinstance(value, int):
                normalized[key] = float(value)
                continue

            if not isinstance(value, float):
                normalized[key] = 0.0
                continue

            if value > 1e6:
                value = 1e6

            if value < -1e6:
                value = -1e6

            normalized[key] = value

        return normalized

    def _ensure_all_features(
        self,
        features: dict[str, float],
    ) -> dict[str, float]:
        return {
            feature_name: features.get(feature_name, 0.0)
            for feature_name in FEATURES
        }