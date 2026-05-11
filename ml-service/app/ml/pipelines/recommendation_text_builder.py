from jinja2 import Template


class RecommendationTextBuilder:
    TEMPLATE = Template(
        """
Оценка пригодности территории: {{ score_percent }}% — {{ level }}.

{% if target %}
Задача пользователя: {{ target }}.
{% endif %}

{{ summary }}

Основные факторы:
{% for reason in reasons %}
- {{ reason }}
{% endfor %}

{% if warnings %}
Ограничения и риски:
{% for warning in warnings %}
- {{ warning }}
{% endfor %}
{% endif %}

Обоснование сформировано на основе связанных объектов справочника: ландшафта, почв, вод, климата, рельефа, фундамента и растительности.
        """.strip()
    )

    def build(
        self,
        *,
        score: float,
        level: str,
        summary: str,
        reasons: list[str],
        warnings: list[str],
        target: str | None,
    ) -> str:
        return self.TEMPLATE.render(
            score_percent=round(score * 100),
            level=level,
            summary=summary,
            reasons=reasons,
            warnings=warnings,
            target=target,
        )