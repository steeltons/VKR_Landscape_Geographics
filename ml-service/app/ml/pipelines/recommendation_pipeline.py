from app.ml.feedback.feedback_corrector import FeedbackCorrector
from app.ml.features.feature_builder import FeatureBuilder
from app.ml.models.model_registry import get_model_registry
from app.ml.pipelines.explanation_builder import ExplanationBuilder


class RecommendationPipeline:

    def __init__(self) -> None:
        self.feature_builder = FeatureBuilder()
        self.model_registry = get_model_registry()
        self.explainer = ExplanationBuilder()
        self.feedback_corrector = FeedbackCorrector()

    def run(self, *, data: dict, task_type: str, target: str | None) -> dict:
        features = self.feature_builder.build(data, task_type=task_type)

        model = self.model_registry.get_model()
        base_score = model.predict_proba(features)

        # --- Apply feedback-aware correction ---
        territory = data.get("territory") or {}
        territory_id = territory.get("id")

        if territory_id is not None:
            corrected_score = self.feedback_corrector.correct(
                territory_id=territory_id,
                task_type=task_type,
                base_score=base_score,
            )
        else:
            corrected_score = base_score

        explanation = self.explainer.build(
            features=features,
            score=corrected_score,
            data=data,
            task_type=task_type,
            target=target,
        )

        return {
            "score": corrected_score,
            "level": explanation["level"],
            "recommendation": explanation["recommendation"],
            "model_version": model.version,
            "features": features,
            "explanation": {
                "summary": explanation["summary"],
                "reasons": explanation["reasons"],
                "warnings": explanation["warnings"],
                "evidence": explanation["evidence"],
            },
        }
