from app.ml.features.feature_builder import FeatureBuilder
from app.ml.models.model_registry import ModelRegistry
from app.ml.pipelines.explanation_builder import ExplanationBuilder


class RecommendationPipeline:

    def __init__(self) -> None:
        self.feature_builder = FeatureBuilder()
        self.model_registry = ModelRegistry()
        self.explainer = ExplanationBuilder()

    def run(self, *, data: dict, task_type: str, target: str | None) -> dict:
        features = self.feature_builder.build(data, task_type=task_type)

        model = self.model_registry.get_model()
        score = model.predict_proba(features)
        explanation = self.explainer.build(features=features, score=score, data=data, task_type=task_type, target=target)


        return {
            "score": score,
            "level": explanation["level"],
            "recommendation": explanation["recommendation"],
            "explanation": {
                "summary": explanation["summary"],
                "reasons": explanation["reasons"],
                "warnings": explanation["warnings"],
                "evidence": explanation["evidence"],
            },
        }