from abc import ABC, abstractmethod


class BaseModel(ABC):
    
    @abstractmethod
    def predict(self, features: dict[str, float | int]) -> float:
        pass

    @abstractmethod
    def predict_proba(self, features: dict[str, float | int]) -> float:
        pass