import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from app.configs.config import settings
from app.ml.training.model_trainer import train_model


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--version",
        default=settings.model_current_version,
        help="Версия модели. Используется как директория в MinIO.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    metrics = train_model(version=args.version)

    print(f"Model uploaded to MinIO: {settings.build_model_object_name(args.version)}")
    print(f"Metrics uploaded to MinIO: {settings.build_metrics_object_name(args.version)}")
    print(f"Dataset uploaded to MinIO: {settings.build_dataset_object_name(args.version)}")

    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()