import hashlib
import math

import pandas as pd


class WeakLabeler:
    def build_labels(self, df: pd.DataFrame) -> pd.DataFrame:
        result = df.copy()

        scores = []

        for _, row in result.iterrows():
            task_type = str(row.get("task_type", "")).lower()

            if task_type == "agriculture":
                score = self._score_agriculture(row)
            elif task_type == "construction":
                score = self._score_construction(row)
            elif task_type == "ecology":
                score = self._score_ecology(row)
            else:
                score = 0.35

            score += self._stable_noise(
                landscape_id=int(row.get("landscape_id", 0)),
                task_type=task_type,
                amplitude=0.08,
            )

            score = self._clip(score, 0.0, 1.0)
            scores.append(score)

        result["target_score"] = scores

        result["target_label"] = result["target_score"].apply(
            self._score_to_label,
        )

        return result

    def _score_agriculture(self, row: pd.Series) -> float:
        score = 0.20

        acidity = self._num(row.get("soil_acidity_mean"))
        soil_count = self._num(row.get("soil_count"))
        has_minerals = self._num(row.get("soil_has_minerals"))
        has_water = self._num(row.get("has_water"))
        has_climate = self._num(row.get("has_climate"))
        plant_count = self._num(row.get("plant_count"))
        relief_count = self._num(row.get("relief_count"))
        kr = self._num(row.get("landscape_kr"))

        if 5.5 <= acidity <= 7.2:
            score += 0.25
        elif 4.8 <= acidity < 5.5 or 7.2 < acidity <= 8.0:
            score += 0.12
        elif acidity > 0:
            score -= 0.08

        if soil_count > 0:
            score += 0.12

        if has_minerals:
            score += 0.08

        if has_water:
            score += 0.10

        if has_climate:
            score += 0.08

        if plant_count > 0:
            score += min(plant_count, 5) * 0.025

        if relief_count > 2:
            score -= 0.05

        if kr > 0:
            score += min(kr, 1.0) * 0.10

        return score

    def _score_construction(self, row: pd.Series) -> float:
        score = 0.25

        foundation_count = self._num(row.get("foundation_count"))
        depth = self._num(row.get("foundation_roof_root_depth_mean"))
        relief_count = self._num(row.get("relief_count"))
        water_count = self._num(row.get("water_count"))
        soil_count = self._num(row.get("soil_count"))
        kr = self._num(row.get("landscape_kr"))

        if foundation_count > 0:
            score += 0.20

        if depth > 0:
            if depth <= 20:
                score += 0.15
            elif depth <= 60:
                score += 0.07
            else:
                score -= 0.05

        if relief_count > 0:
            score += 0.05

        if water_count > 0:
            score -= 0.08

        if soil_count > 0:
            score += 0.05

        if kr > 0:
            score += min(kr, 1.0) * 0.08

        return score

    def _score_ecology(self, row: pd.Series) -> float:
        score = 0.25

        plant_count = self._num(row.get("plant_count"))
        water_count = self._num(row.get("water_count"))
        climate_count = self._num(row.get("climate_count"))
        soil_count = self._num(row.get("soil_count"))
        relief_count = self._num(row.get("relief_count"))
        kr = self._num(row.get("landscape_kr"))

        if plant_count > 0:
            score += min(plant_count, 8) * 0.04

        if water_count > 0:
            score += min(water_count, 3) * 0.06

        if climate_count > 0:
            score += 0.08

        if soil_count > 0:
            score += 0.06

        if relief_count > 0:
            score += 0.04

        if kr > 0:
            score += min(kr, 1.0) * 0.10

        return score

    def _score_to_label(self, score: float) -> int:
        if score < 0.4:
            return 0

        if score < 0.7:
            return 1

        return 2

    def _stable_noise(
        self,
        *,
        landscape_id: int,
        task_type: str,
        amplitude: float,
    ) -> float:
        raw = f"{landscape_id}:{task_type}".encode("utf-8")
        digest = hashlib.md5(raw).hexdigest()

        value = int(digest[:8], 16) / 0xFFFFFFFF

        return (value - 0.5) * 2 * amplitude

    def _num(self, value) -> float:
        try:
            if value is None or math.isnan(float(value)):
                return 0.0
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    def _clip(self, value: float, min_value: float, max_value: float) -> float:
        return max(min_value, min(value, max_value))