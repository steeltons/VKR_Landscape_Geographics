import json
import logging
import re
from typing import Any

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    PreTrainedModel,
    PreTrainedTokenizer,
)

from app.ml.llm.config import llm_settings
from app.ml.llm.prompt_builder import (
    SYSTEM_PROMPT,
    apply_chat_template,
    build_prompt,
)


logger = logging.getLogger(__name__)


class LLMService:
    """Сервис для инференса локальной LLM (Qwen2.5 / TinyLlama и т.п.).

    Модель загружается lazy — при первом вызове generate().
    """

    def __init__(self) -> None:
        self._model: PreTrainedModel | None = None
        self._tokenizer: PreTrainedTokenizer | None = None
        self._is_loaded: bool = False
        self._load_attempted: bool = False

    # --- Public API ---

    def generate_explanation(
        self,
        *,
        features: dict[str, float],
        evidence: list[dict[str, Any]],
        score: float,
        task_type: str,
        level: str,
        target: str | None,
    ) -> dict[str, Any] | None:
        """Сгенерировать объяснение через LLM.

        Возвращает словарь с ключами: summary, reasons, warnings, recommendation.
        Если генерация не удалась — возвращает None.
        """
        if not self._ensure_model_loaded():
            logger.warning("LLM model not available, falling back to None")
            return None

        user_prompt = build_prompt(
            features=features,
            evidence=evidence,
            score=score,
            task_type=task_type,
            level=level,
            target=target,
        )

        full_prompt = apply_chat_template(
            model_name=llm_settings.model_name,
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )

        try:
            raw_output = self._generate(full_prompt)
            parsed = self._parse_json_response(raw_output)
            return parsed
        except Exception:
            logger.exception("LLM generation failed")
            return None

    # --- Model lifecycle ---

    def _ensure_model_loaded(self) -> bool:
        if self._is_loaded:
            return True

        if self._load_attempted:
            return False

        self._load_attempted = True

        try:
            self._load_model()
            self._is_loaded = True
            return True
        except Exception:
            logger.exception("Failed to load LLM model '%s'", llm_settings.model_name)
            return False

    def _load_model(self) -> None:
        logger.info(
            "START LLMService::_load_model model=%s device=%s",
            llm_settings.model_name,
            llm_settings.device,
        )

        quantization_config = self._build_quantization_config()

        logger.info(
            "Loading tokenizer for %s ...",
            llm_settings.model_name,
        )
        self._tokenizer = AutoTokenizer.from_pretrained(
            llm_settings.model_name,
            cache_dir=llm_settings.cache_dir,
            trust_remote_code=False,
        )

        # Устанавливаем pad_token, если его нет
        if self._tokenizer.pad_token is None:
            self._tokenizer.pad_token = self._tokenizer.eos_token

        logger.info(
            "Loading model %s (this may take a while on CPU)...",
            llm_settings.model_name,
        )

        self._model = AutoModelForCausalLM.from_pretrained(
            llm_settings.model_name,
            quantization_config=quantization_config,
            device_map=llm_settings.device,  # "cpu" или "auto"
            torch_dtype=torch.float32 if llm_settings.device == "cpu" else torch.float16,
            cache_dir=llm_settings.cache_dir,
            trust_remote_code=False,
            low_cpu_mem_usage=True,
        )

        # Переключаем модель в eval mode
        self._model.eval()

        logger.info(
            "END LLMService::_load_model model=%s loaded successfully",
            llm_settings.model_name,
        )

    def _build_quantization_config(self) -> BitsAndBytesConfig | None:
        if llm_settings.load_in_4bit:
            logger.info("Using 4-bit quantization")
            return BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float32,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
            )

        if llm_settings.load_in_8bit:
            logger.info("Using 8-bit quantization")
            return BitsAndBytesConfig(load_in_8bit=True)

        return None

    # --- Inference ---

    def _generate(self, prompt: str) -> str:
        if self._model is None or self._tokenizer is None:
            raise RuntimeError("LLM model is not loaded")

        inputs = self._tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=llm_settings.prompt_max_context_length,
        ).to(llm_settings.device)

        with torch.no_grad():
            outputs = self._model.generate(
                **inputs,
                max_new_tokens=llm_settings.max_new_tokens,
                temperature=llm_settings.temperature,
                top_p=llm_settings.top_p,
                repetition_penalty=llm_settings.repetition_penalty,
                do_sample=True,
                pad_token_id=self._tokenizer.pad_token_id,
                eos_token_id=self._tokenizer.eos_token_id,
            )

        # Декодируем только новые токены (после промпта)
        prompt_length = inputs["input_ids"].shape[1]
        new_tokens = outputs[0][prompt_length:]
        response = self._tokenizer.decode(new_tokens, skip_special_tokens=True)

        return response.strip()

    # --- Response parsing ---

    def _parse_json_response(self, raw: str) -> dict[str, Any] | None:
        """Пытается извлечь JSON из ответа модели.

        Модель может вернуть:
        - Чистый JSON: {"summary": "...", "reasons": [...], ...}
        - JSON в markdown-блоке: ```json ... ```
        - Текст с вкраплениями JSON.
        """
        # Сначала пытаемся найти ```json ... ``` блок
        json_block_match = re.search(
            r"```(?:json)?\s*\n?(.*?)\n?```",
            raw,
            re.DOTALL,
        )

        json_str = json_block_match.group(1) if json_block_match else raw

        # Пытаемся спарсить как JSON
        try:
            result = json.loads(json_str)
        except json.JSONDecodeError:
            # Пробуем найти откурывающуюся { и закрывающуюся }
            brace_match = re.search(r"\{.*\}", json_str, re.DOTALL)
            if brace_match:
                try:
                    result = json.loads(brace_match.group(0))
                except json.JSONDecodeError:
                    logger.warning("Failed to parse LLM response as JSON: %s", raw[:200])
                    return None
            else:
                logger.warning("No JSON found in LLM response: %s", raw[:200])
                return None

        # Валидируем структуру
        if not isinstance(result, dict):
            logger.warning("LLM response is not a dict: %s", result)
            return None

        required_keys = {"summary", "reasons", "warnings", "recommendation"}
        missing = required_keys - set(result.keys())
        if missing:
            logger.warning(
                "LLM response missing keys: %s. Got: %s",
                missing,
                list(result.keys()),
            )
            return None

        # Приводим типы
        if not isinstance(result.get("reasons"), list):
            result["reasons"] = [str(result.get("reasons", ""))]
        if not isinstance(result.get("warnings"), list):
            result["warnings"] = [str(result.get("warnings", ""))] if result.get("warnings") else []

        return result


# --- Global singleton ---

_llm_service: LLMService | None = None


def get_llm_service() -> LLMService:
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
