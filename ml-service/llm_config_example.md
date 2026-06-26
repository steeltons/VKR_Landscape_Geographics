# Настройки LLM для ML-Service

## Переменные окружения (префикс `LLM_`)

Эти переменные можно добавить в `.env` файл проекта или передать как переменные окружения.

```env
# --- Выбор модели ---
# Qwen2.5-0.5B-Instruct — ~0.5B параметров, ~1GB в full precision,
# ~400MB в 4-bit. Отлично работает на CPU с 4GB RAM.
# Альтернативы:
#   "Qwen/Qwen2.5-1.5B-Instruct"  (~1.5B, ~3GB full)
#   "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  (~1.1B, ~2.2GB full)
#   "microsoft/Phi-3-mini-4k-instruct"     (~3.8B, нужно >4GB)
LLM_MODEL_NAME=Qwen/Qwen2.5-0.5B-Instruct

# Устройство: "cpu" (без GPU) или "cuda" (NVIDIA)
LLM_DEVICE=cpu

# Квантизация (экономия памяти):
# Для CPU: load_in_4bit=false — 4-bit не даёт прироста скорости на CPU
# Для GPU: load_in_4bit=true — ~4x сжатие модели
LLM_LOAD_IN_4BIT=false
LLM_LOAD_IN_8BIT=false

# Параметры генерации
LLM_MAX_NEW_TOKENS=512
LLM_TEMPERATURE=0.3
LLM_TOP_P=0.9
LLM_REPETITION_PENALTY=1.1

# Максимальная длина входного контекста (токенов)
LLM_PROMPT_MAX_CONTEXT_LENGTH=2048

# Путь к кешу HuggingFace (опционально)
# LLM_CACHE_DIR=/path/to/huggingface/cache
```

## Первый запуск

При первом вызове рекомендации модель скачается с HuggingFace Hub автоматически (~500MB для Qwen2.5-0.5B).

Если модель не найдена или загрузка не удалась — сервис автоматически переключится на rule-based объяснение (fallback).
