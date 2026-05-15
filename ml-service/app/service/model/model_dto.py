from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ModelTrainRqDto(BaseModel):
    version: str = Field(min_length=1, max_length=128)
    reload_after_train: bool = False


class ModelTrainRsDto(BaseModel):
    version: str
    model_object_name: str
    metrics_object_name: str
    dataset_object_name: str
    metrics: dict[str, Any]


class ModelMetadataRsDto(BaseModel):
    version: str
    is_actual: bool

    model_object_name: str
    metrics_object_name: str
    dataset_object_name: str

    model_exists: bool
    metrics_exists: bool
    dataset_exists: bool

    model_last_modified: datetime | None = None

    dataset_size: int | None = None
    train_size: int | None = None
    test_size: int | None = None

    target_score_min: float | None = None
    target_score_max: float | None = None
    target_score_mean: float | None = None

    mae: float | None = None
    mse: float | None = None
    rmse: float | None = None
    r2: float | None = None

    features: list[str] = []
    label_distribution: dict[str, int] = {}