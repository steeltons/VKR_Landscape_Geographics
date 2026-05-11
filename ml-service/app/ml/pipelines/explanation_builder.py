from app.ml.pipelines.evidence_builder import EvidenceBuilder
from app.ml.pipelines.recommendation_text_builder import RecommendationTextBuilder


class ExplanationBuilder:
    def __init__(self) -> None:
        self.evidence_builder = EvidenceBuilder()
        self.text_builder = RecommendationTextBuilder()

    def build(
        self,
        *,
        features: dict,
        score: float,
        data: dict,
        task_type: str,
        target: str | None,
    ) -> dict:
        reasons: list[str] = []
        warnings: list[str] = []

        level = self._build_level(score)
        summary = self._build_summary(score, task_type)

        self._append_common_reasons(
            features=features,
            reasons=reasons,
            warnings=warnings,
        )

        self._append_task_specific_reasons(
            features=features,
            task_type=task_type,
            reasons=reasons,
            warnings=warnings,
        )

        evidence = self.evidence_builder.build(
            data=data,
            features=features,
            task_type=task_type,
        )

        recommendation = self.text_builder.build(
            score=score,
            level=level,
            summary=summary,
            reasons=reasons,
            warnings=warnings,
            target=target,
        )

        return {
            "summary": summary,
            "level": level,
            "recommendation": recommendation,
            "reasons": reasons,
            "warnings": warnings,
            "evidence": evidence,
        }

    def _build_level(self, score: float) -> str:
        if score >= 0.75:
            return "хорошо подходит"

        if score >= 0.5:
            return "условно подходит"

        if score >= 0.35:
            return "ограниченно подходит"

        return "слабо подходит"

    def _build_summary(
        self,
        score: float,
        task_type: str,
    ) -> str:
        task_title = self._task_title(task_type)

        if score >= 0.75:
            return f"Территория имеет высокую пригодность для задачи: {task_title}."

        if score >= 0.5:
            return f"Территория может быть использована для задачи: {task_title}, но требует учёта ограничений."

        if score >= 0.35:
            return f"Территория имеет ограниченную пригодность для задачи: {task_title}."

        return f"Территория слабо подходит для задачи: {task_title}."

    def _append_common_reasons(
        self,
        *,
        features: dict,
        reasons: list[str],
        warnings: list[str],
    ) -> None:
        if features.get("has_landscape", 0) > 0:
            reasons.append("Определён связанный ландшафт территории")

        if features.get("soil_count", 0) > 0:
            reasons.append("Найдены связанные почвенные характеристики")

        if features.get("has_climate", 0) > 0:
            reasons.append("Климатические условия учтены при оценке")
        else:
            warnings.append("Нет связанных климатических характеристик")

        if features.get("has_water", 0) > 0:
            reasons.append("Водный компонент территории учтён при оценке")

        if features.get("has_plants", 0) > 0:
            reasons.append("Растительность использована как индикатор природных условий")

    def _append_task_specific_reasons(
        self,
        *,
        features: dict,
        task_type: str,
        reasons: list[str],
        warnings: list[str],
    ) -> None:
        task_type = task_type.lower().strip()

        if task_type == "agriculture":
            self._append_agriculture_reasons(features, reasons, warnings)
            return

        if task_type == "construction":
            self._append_construction_reasons(features, reasons, warnings)
            return

        if task_type == "ecology":
            self._append_ecology_reasons(features, reasons, warnings)
            return

        warnings.append("Тип задачи не распознан, использована общая оценка территории")

    def _append_agriculture_reasons(
        self,
        features: dict,
        reasons: list[str],
        warnings: list[str],
    ) -> None:
        acidity = float(features.get("soil_acidity_mean", 0.0) or 0.0)

        if 5.5 <= acidity <= 7.2:
            reasons.append("Средняя кислотность почв находится в благоприятном диапазоне для выращивания растений")
        elif acidity > 0:
            warnings.append("Кислотность почв может ограничивать выращивание отдельных культур")
        else:
            warnings.append("Нет числовых данных по кислотности почв")

        if features.get("has_water", 0) <= 0:
            warnings.append("Нет связанных данных по водному компоненту территории")

    def _append_construction_reasons(
        self,
        features: dict,
        reasons: list[str],
        warnings: list[str],
    ) -> None:
        foundation_count = features.get("foundation_count", 0)
        depth = features.get("foundation_roof_root_depth_mean", 0)

        if foundation_count > 0:
            reasons.append("Есть данные о фундаменте ландшафта")
        else:
            warnings.append("Нет связанных данных о фундаменте ландшафта")

        if depth and depth <= 20:
            reasons.append("Средняя глубина залегания фундамента выглядит благоприятной для инженерной оценки")
        elif depth and depth > 60:
            warnings.append("Большая глубина залегания фундамента может усложнять строительное освоение")

        if features.get("has_water", 0) > 0:
            warnings.append("Водный режим может повышать инженерные риски")

    def _append_ecology_reasons(
        self,
        features: dict,
        reasons: list[str],
        warnings: list[str],
    ) -> None:
        if features.get("plant_count", 0) > 0:
            reasons.append("Растительность повышает экологическую информативность территории")

        if features.get("water_count", 0) > 0:
            reasons.append("Водные компоненты повышают экологическую значимость территории")

        if features.get("relief_count", 0) > 0:
            reasons.append("Рельеф учитывается как фактор природного разнообразия")

    def _task_title(self, task_type: str) -> str:
        mapping = {
            "agriculture": "сельскохозяйственная оценка и выращивание растений",
            "construction": "строительная и инженерная оценка",
            "ecology": "экологическая оценка территории",
        }

        return mapping.get(task_type.lower().strip(), task_type)