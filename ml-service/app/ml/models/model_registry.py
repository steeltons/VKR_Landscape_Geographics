from app.ml.models.catboost_model import CatBoostModel
from app.ml.models.base_model import BaseModel


class ModelRegistry:

    def __init__(self) -> None:
        self._models: dict[str, BaseModel] = {}

    def get_model(self, name: str = "default") -> BaseModel:
        if name not in self._models:
            if name == "default":
                self._models[name] = CatBoostModel()
            else:
                raise ValueError(f"Unknown model: {name}")

        return self._models[name]