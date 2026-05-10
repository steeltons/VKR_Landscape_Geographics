class ExplanationBuilder:

    def build(self, *, features: dict, score: float, data: dict) -> dict:
        reasons: list[str] = []
        warnings: list[str] = []

        acidity = features.get("soil_acidity")

        if acidity:
            if 5.5 <= acidity <= 7.5:
                reasons.append("Оптимальная кислотность почвы")
            else:
                warnings.append("Кислотность почвы может быть неблагоприятной")

        humidity = features.get("ground_humidity")

        if humidity:
            if 30 <= humidity <= 70:
                reasons.append("Подходящая влажность грунта")
            else:
                warnings.append("Нестабильная влажность грунта")

        if data.get("climates"):
            reasons.append("Климат учтён при анализе")
        else:
            warnings.append("Нет данных о климате")

        if score >= 0.75:
            summary = "Территория хорошо подходит для выбранной задачи"
        elif score >= 0.5:
            summary = "Территория условно подходит, есть ограничения"
        else:
            summary = "Территория слабо подходит для выбранной задачи"

        return {
            "summary": summary,
            "reasons": reasons,
            "warnings": warnings,
        }