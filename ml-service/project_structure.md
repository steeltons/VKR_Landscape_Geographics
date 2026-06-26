# Project Structure

```text
./
├── requirements.txt
├── structure_script.py
├── project_structure.md
├── .env
└── .env.example
├── scripts/
│   └── train.py
├── catboost_info/
│   └── test/
│   └── learn/
│   └── tmp/
├── app/
│   ├── main.py
│   └── __init__.py
│   ├── service/
│   │   └── __init__.py
│   │   ├── health/
│   │   │   ├── health_controller.py
│   │   │   └── __init__.py
│   │   ├── recommendation/
│   │   │   ├── recommendation_service.py
│   │   │   ├── __init__.py
│   │   │   ├── recommendation_controller.py
│   │   │   ├── recommendation_dto.py
│   │   │   └── recommendation_dto_mapper.py
│   │   ├── model/
│   │   │   ├── model_service.py
│   │   │   ├── __init__.py
│   │   │   ├── model_dto.py
│   │   │   └── model_controller.py
│   ├── ml/
│   │   └── __init__.py
│   │   ├── features/
│   │   │   ├── feature_builder.py
│   │   │   ├── encoders.py
│   │   │   ├── __init__.py
│   │   │   └── feature_schema.py
│   │   ├── artifacts/
│   │   │   ├── model_artifact_storage.py
│   │   │   └── __init__.py
│   │   ├── models/
│   │   │   ├── model_registry.py
│   │   │   ├── catboost_model.py
│   │   │   ├── base_model.py
│   │   │   └── __init__.py
│   │   ├── pipelines/
│   │   │   ├── evidence_builder.py
│   │   │   ├── recommendation_pipeline.py
│   │   │   ├── explanation_builder.py
│   │   │   ├── __init__.py
│   │   │   └── recommendation_text_builder.py
│   │   ├── training/
│   │   │   ├── model_trainer.py
│   │   │   ├── weak_labeler.py
│   │   │   ├── __init__.py
│   │   │   └── dataset_builder.py
│   ├── persistence/
│   │   ├── dictionary_microservice_client.py
│   │   └── __init__.py
│   ├── configs/
│   │   ├── __init__.py
│   │   └── config.py
```