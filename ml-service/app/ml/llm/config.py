from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_prefix="LLM_",
    )

    model_name: str = "Qwen/Qwen2.5-0.5B-Instruct"
    """HuggingFace model identifier or local path to the model."""

    device: str = "cpu"
    """Device for inference: 'cpu' or 'cuda'."""

    load_in_4bit: bool = False
    """Whether to load model in 4-bit quantized mode. Forces CPU offload if on CPU."""

    load_in_8bit: bool = False
    """Whether to load model in 8-bit quantized mode."""

    max_new_tokens: int = 512
    """Maximum number of tokens to generate in a single response."""

    temperature: float = 0.3
    """Sampling temperature. Lower = more deterministic."""

    top_p: float = 0.9
    """Nucleus sampling parameter."""

    repetition_penalty: float = 1.1
    """Penalty for repeating tokens."""

    cache_dir: str | None = None
    """Optional local cache directory for model files."""

    prompt_max_context_length: int = 2048
    """Maximum number of input tokens (system + user prompt) before truncation."""

    @property
    def model_short_name(self) -> str:
        return self.model_name.split("/")[-1]


llm_settings = LLMSettings()
