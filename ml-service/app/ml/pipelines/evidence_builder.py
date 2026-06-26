from typing import Any


class EvidenceBuilder:
    API_PREFIX = "/api/v1/dictionary"

    ROUTES = {
        "landscape": "landscapes",
        "soil": "soils",
        "ground": "grounds",
        "plant": "plants",
        "relief": "reliefs",
        "foundation": "foundations",
        "water": "waters",
        "climate": "climates",
    }

    def build(
        self,
        *,
        data: dict,
        features: dict[str, float],
        task_type: str,
    ) -> list[dict[str, Any]]:
        task_type = task_type.lower().strip()

        evidence: list[dict[str, Any]] = []

        landscape = data.get("landscape")
        if landscape:
            evidence.append(
                self._make_evidence(
                    object_type="landscape",
                    obj=landscape,
                    impact="neutral",
                    factor="landscape",
                    reason="Ландшафт является базовым объектом оценки территории",
                )
            )

        evidence.extend(
            self._build_soil_evidence(
                soils=data.get("soils") or [],
                task_type=task_type,
            )
        )

        evidence.extend(
            self._build_water_evidence(
                waters=data.get("waters") or [],
                task_type=task_type,
            )
        )

        evidence.extend(
            self._build_climate_evidence(
                climates=data.get("climates") or [],
                task_type=task_type,
            )
        )

        evidence.extend(
            self._build_relief_evidence(
                reliefs=data.get("reliefs") or [],
                task_type=task_type,
            )
        )

        evidence.extend(
            self._build_foundation_evidence(
                foundations=data.get("foundations") or [],
                task_type=task_type,
            )
        )

        evidence.extend(
            self._build_plant_evidence(
                plants=data.get("plants") or [],
                task_type=task_type,
            )
        )

        return evidence

    def _build_soil_evidence(
        self,
        *,
        soils: list[dict],
        task_type: str,
    ) -> list[dict]:
        result = []

        for soil in soils:
            acidity = self._to_float(soil.get("acidity"), default=None)

            if task_type == "agriculture":
                if acidity is None:
                    impact = "neutral"
                    reason = "Почва учитывается при оценке, но числовое значение кислотности отсутствует"
                elif 5.5 <= acidity <= 7.2:
                    impact = "positive"
                    reason = "Кислотность почвы находится в благоприятном диапазоне для выращивания растений"
                elif 4.8 <= acidity < 5.5 or 7.2 < acidity <= 8.0:
                    impact = "neutral"
                    reason = "Кислотность почвы допустима, но может требовать уточнения под конкретную культуру"
                else:
                    impact = "negative"
                    reason = "Кислотность почвы может быть ограничивающим фактором для выращивания растений"
            else:
                impact = "neutral"
                reason = "Почвенные характеристики учитываются как часть описания ландшафта"

            result.append(
                self._make_evidence(
                    object_type="soil",
                    obj=soil,
                    impact=impact,
                    factor="soil_acidity",
                    reason=reason,
                )
            )

        return result

    def _build_water_evidence(
        self,
        *,
        waters: list[dict],
        task_type: str,
    ) -> list[dict]:
        result = []

        for water in waters:
            if task_type == "agriculture":
                impact = "positive"
                reason = "Наличие водного компонента повышает значимость территории для сельскохозяйственной оценки"
            elif task_type == "construction":
                impact = "negative"
                reason = "Водный режим может повышать инженерные риски при строительстве"
            elif task_type == "ecology":
                impact = "positive"
                reason = "Водные объекты повышают экологическую значимость территории"
            else:
                impact = "neutral"
                reason = "Водный компонент учитывается при общей оценке территории"

            result.append(
                self._make_evidence(
                    object_type="water",
                    obj=water,
                    impact=impact,
                    factor="water",
                    reason=reason,
                )
            )

        return result

    def _build_climate_evidence(
        self,
        *,
        climates: list[dict],
        task_type: str,
    ) -> list[dict]:
        return [
            self._make_evidence(
                object_type="climate",
                obj=climate,
                impact="positive",
                factor="climate",
                reason="Климатическая характеристика использована при расчёте пригодности территории",
            )
            for climate in climates
        ]

    def _build_relief_evidence(
        self,
        *,
        reliefs: list[dict],
        task_type: str,
    ) -> list[dict]:
        result = []

        for relief in reliefs:
            if task_type == "construction":
                impact = "neutral"
                reason = "Рельеф влияет на инженерную пригодность и сложность освоения территории"
            elif task_type == "agriculture":
                impact = "neutral"
                reason = "Рельеф может влиять на водный режим, эрозионные процессы и освоение территории"
            else:
                impact = "positive"
                reason = "Рельеф учитывается как фактор природного разнообразия территории"

            result.append(
                self._make_evidence(
                    object_type="relief",
                    obj=relief,
                    impact=impact,
                    factor="relief",
                    reason=reason,
                )
            )

        return result

    def _build_foundation_evidence(
        self,
        *,
        foundations: list[dict],
        task_type: str,
    ) -> list[dict]:
        result = []

        for foundation in foundations:
            depth = self._to_float(
                foundation.get("roof_root_depth"),
                default=None,
            )

            if task_type == "construction":
                if depth is None:
                    impact = "neutral"
                    reason = "Фундамент учитывается, но глубина залегания не указана"
                elif depth <= 20:
                    impact = "positive"
                    reason = "Относительно небольшая глубина залегания фундамента может быть благоприятной для инженерной оценки"
                elif depth <= 60:
                    impact = "neutral"
                    reason = "Средняя глубина залегания фундамента требует дополнительного инженерного анализа"
                else:
                    impact = "negative"
                    reason = "Большая глубина залегания фундамента может усложнять строительное освоение"
            else:
                impact = "neutral"
                reason = "Фундамент учитывается как геологическая основа ландшафта"

            result.append(
                self._make_evidence(
                    object_type="foundation",
                    obj=foundation,
                    impact=impact,
                    factor="foundation_roof_root_depth",
                    reason=reason,
                )
            )

        return result

    def _build_plant_evidence(
        self,
        *,
        plants: list[dict],
        task_type: str,
    ) -> list[dict]:
        result = []

        for plant in plants:
            if task_type == "ecology":
                impact = "positive"
                reason = "Растительность повышает экологическую информативность и природную ценность территории"
            elif task_type == "agriculture":
                impact = "positive"
                reason = "Растительность использована как индикатор условий произрастания"
            else:
                impact = "neutral"
                reason = "Растительность учитывается как компонент ландшафта"

            result.append(
                self._make_evidence(
                    object_type="plant",
                    obj=plant,
                    impact=impact,
                    factor="plant",
                    reason=reason,
                )
            )

        return result

    def _make_evidence(
        self,
        *,
        object_type: str,
        obj: dict,
        impact: str,
        factor: str,
        reason: str,
    ) -> dict[str, Any]:
        object_id = obj.get("id")
        title = obj.get("name") or f"{object_type} #{object_id}"

        return {
            "object_type": object_type,
            "object_id": object_id,
            "title": title,
            "api_path": self._build_api_path(object_type, object_id),
            "impact": impact,
            "factor": factor,
            "reason": reason,
        }

    def _build_api_path(
        self,
        object_type: str,
        object_id: int | None,
    ) -> str:
        route = self.ROUTES.get(object_type, object_type)

        if object_id is None:
            return f"{self.API_PREFIX}/{route}"

        return f"{self.API_PREFIX}/{route}/{object_id}"

    def _to_float(
        self,
        value: Any,
        default: float | None = 0.0,
    ) -> float | None:
        if value is None:
            return default

        try:
            return float(str(value).replace(",", "."))
        except (TypeError, ValueError):
            return default