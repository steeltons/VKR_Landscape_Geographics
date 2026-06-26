import logging
from typing import Any

from app.ml.llm.config import llm_settings


logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """Ты — эксперт-географ и агроном в геоинформационной системе оценки ландшафтов. Твоя задача — анализировать числовые признаки территории, скоринг модели и связанные объекты, затем давать объяснимую, человекочитаемую рекомендацию на русском языке.

Ты должен:
1. Написать краткое саммари (summary) пригодности территории для указанной задачи.
2. Перечислить 2–4 ключевых фактора (reasons), повлиявших на оценку — на основе переданных признаков и объектов территории.
3. Указать 1–3 ограничения или предупреждения (warnings), если они есть.
4. Написать связный текст рекомендации (recommendation), который резюмирует оценку.

Правила:
- Всегда пиши на русском языке.
- Будь конкретным и фактологичным, ссылайся на переданные данные.
- Если каких-то данных нет — не выдумывай, скажи что данные отсутствуют.
- Не используй markdown-разметку, пиши чистыми абзацами.
- Ответ должен строго соответствовать JSON-схеме ниже."""


def format_evidence_for_prompt(evidence: list[dict[str, Any]]) -> str:
    """Форматирует список evidence в краткое текстовое представление для промпта."""
    if not evidence:
        return "Нет связанных объектов справочника."

    lines = []
    for item in evidence:
        obj_type = item.get("object_type", "?")
        title = item.get("title", "?")
        impact = item.get("impact", "neutral")
        reason = item.get("reason", "")
        lines.append(f"- [{obj_type}] {title} (влияние: {impact}) — {reason}")

    return "\n".join(lines)


def format_features_for_prompt(features: dict[str, float]) -> str:
    """Форматирует словарь признаков в читаемый текст."""
    if not features:
        return "Нет данных о числовых признаках."

    lines = []
    for key, value in features.items():
        if abs(value) < 0.0001 and key not in (
            "has_landscape", "has_territory", "has_climate",
            "has_water", "has_plants", "has_foundation", "has_relief",
        ):
            continue
        lines.append(f"- {key}: {value:.4f}" if isinstance(value, float) else f"- {key}: {value}")

    return "\n".join(lines)


def build_prompt(
    *,
    features: dict[str, float],
    evidence: list[dict[str, Any]],
    score: float,
    task_type: str,
    level: str,
    target: str | None,
) -> str:
    """Собирает полный промпт для LLM (system + user) в формате chat template."""

    task_title_map = {
        "agriculture": "сельскохозяйственная оценка и пригодность для выращивания растений",
        "construction": "строительная и инженерная оценка пригодности территории",
        "ecology": "экологическая оценка ценности территории",
    }
    task_title = task_title_map.get(task_type.lower(), task_type)

    target_line = f"\nЦель пользователя: {target}." if target else ""

    features_text = format_features_for_prompt(features)
    evidence_text = format_evidence_for_prompt(evidence)

    user_prompt = f"""Проанализируй территорию и дай рекомендацию.

Тип задачи: {task_title}.{target_line}
Числовой скоринг модели: {score:.4f} (от 0 до 1, где 1 — максимальная пригодность).
Уровень пригодности: {level}.

Числовые признаки территории:
{features_text}

Связанные объекты справочника:
{evidence_text}

На основе этих данных сформируй ответ строго в формате JSON с ключами:
- "summary" (строка, 1-2 предложения),
- "reasons" (список строк, 2-4 фактора),
- "warnings" (список строк, 0-3 предупреждения),
- "recommendation" (строка, 3-5 предложений, связный текст-резюме).

Только JSON, без дополнительного текста."""

    return user_prompt


def apply_chat_template(model_name: str, system_prompt: str, user_prompt: str) -> str:
    """Применяет chat-template, известный для модели, или стандартный для Qwen."""
    # Qwen2.5 использует стандартный chatml формат
    return f"<|system|>\n{system_prompt}\n<|user|>\n{user_prompt}\n<|assistant|>\n"
