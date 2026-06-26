import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Any

from olms_minio_component.exceptions import OlmsMinioFileNotFoundError
from olms_minio_component import OlmsMinioComponent

from app.configs.config import settings


logger = logging.getLogger(__name__)


class ModelArtifactStorage:
    def __init__(self) -> None:
        self.minio_component = OlmsMinioComponent()
        self.local_tmp_dir = Path(settings.model_local_tmp_dir)
        self.local_tmp_dir.mkdir(parents=True, exist_ok=True)

    def get_current_model_version(self) -> str:
        object_name = settings.build_current_model_version_object_name()

        logger.info("START ModelArtifactStorage::get_current_model_version object_name=%s", object_name)

        try:
            content = self.minio_component.download_bytes(object_name=object_name)
        except OlmsMinioFileNotFoundError:
            logger.warning(
                "Current model marker not found in MinIO. Fallback to settings.model_current_version=%s",
                settings.model_current_version,
            )
            return settings.model_current_version

        data = json.loads(content.decode("utf-8"))
        version = str(data.get("version") or "").strip()

        if not version:
            logger.warning(
                "Current model marker is empty. Fallback to settings.model_current_version=%s",
                settings.model_current_version,
            )
            return settings.model_current_version

        logger.info("END ModelArtifactStorage::get_current_model_version version=%s", version)

        return version

    def set_current_model_version(self, *, version: str) -> None:
        object_name = settings.build_current_model_version_object_name()

        content = json.dumps({"version": version}, ensure_ascii=False, indent=2).encode("utf-8")

        logger.info(
            "START ModelArtifactStorage::set_current_model_version version=%s object_name=%s",
            version,
            object_name,
        )

        self.minio_component.upload_bytes(
            content=content,
            original_filename=settings.model_current_version_filename,
            file_group="ml_model_current_version",
            content_type="application/json",
            object_name=object_name,
            metadata={"artifact-type": "current-model-version", "model-version": version},
        )

        logger.info("END ModelArtifactStorage::set_current_model_version version=%s", version)

    def download_model_to_local_file(self, *, version: str | None = None) -> Path:
        model_version = version or self.get_current_model_version()
        object_name = settings.build_model_object_name(model_version)
        local_path = self._build_local_model_path(model_version)

        logger.info(
            "START ModelArtifactStorage::download_model_to_local_file version=%s object_name=%s",
            model_version,
            object_name,
        )

        content = self.minio_component.download_bytes(object_name=object_name)

        local_path.parent.mkdir(parents=True, exist_ok=True)
        local_path.write_bytes(content)

        logger.info(
            "END ModelArtifactStorage::download_model_to_local_file version=%s local_path=%s",
            model_version,
            local_path,
        )

        return local_path

    def upload_model_artifacts(
        self,
        *,
        version: str,
        model_path: Path,
        metrics_path: Path | None = None,
        dataset_path: Path | None = None,
    ) -> None:
        logger.info("START ModelArtifactStorage::upload_model_artifacts version=%s", version)

        self.upload_model(version=version, model_path=model_path)

        if metrics_path is not None:
            self.upload_metrics(version=version, metrics_path=metrics_path)

        if dataset_path is not None:
            self.upload_dataset(version=version, dataset_path=dataset_path)

        logger.info("END ModelArtifactStorage::upload_model_artifacts version=%s", version)

    def upload_model(self, *, version: str, model_path: Path) -> None:
        self._upload_file(
            local_path=model_path,
            object_name=settings.build_model_object_name(version),
            content_type="application/octet-stream",
            file_group="ml_model",
        )

    def upload_metrics(self, *, version: str, metrics_path: Path) -> None:
        self._upload_file(
            local_path=metrics_path,
            object_name=settings.build_metrics_object_name(version),
            content_type="application/json",
            file_group="ml_model_metrics",
        )

    def upload_dataset(self, *, version: str, dataset_path: Path) -> None:
        self._upload_file(
            local_path=dataset_path,
            object_name=settings.build_dataset_object_name(version),
            content_type="text/csv",
            file_group="ml_training_dataset",
        )

    def get_model_metadata(self, *, version: str) -> dict[str, Any]:
        actual_version = self.get_current_model_version()

        model_object_name = settings.build_model_object_name(version)
        metrics_object_name = settings.build_metrics_object_name(version)
        dataset_object_name = settings.build_dataset_object_name(version)

        metrics = self.download_metrics_dict(version=version)
        model_stat = self._safe_stat_object(model_object_name)

        return {
            "version": version,
            "is_actual": version == actual_version,
            "model_object_name": model_object_name,
            "metrics_object_name": metrics_object_name,
            "dataset_object_name": dataset_object_name,
            "model_exists": model_stat is not None,
            "metrics_exists": self._safe_object_exists(metrics_object_name),
            "dataset_exists": self._safe_object_exists(dataset_object_name),
            "model_last_modified": model_stat.last_modified if model_stat is not None else None,
            "dataset_size": self._to_int_or_none(metrics.get("dataset_size")),
            "train_size": self._to_int_or_none(metrics.get("train_size")),
            "test_size": self._to_int_or_none(metrics.get("test_size")),
            "target_score_min": self._to_float_or_none(metrics.get("target_score_min")),
            "target_score_max": self._to_float_or_none(metrics.get("target_score_max")),
            "target_score_mean": self._to_float_or_none(metrics.get("target_score_mean")),
            "mae": self._to_float_or_none(metrics.get("mae")),
            "mse": self._to_float_or_none(metrics.get("mse")),
            "rmse": self._to_float_or_none(metrics.get("rmse")),
            "r2": self._to_float_or_none(metrics.get("r2")),
            "features": metrics.get("features") or [],
            "label_distribution": metrics.get("label_distribution") or {},
        }

    def get_actual_model_metadata(self) -> dict[str, Any]:
        version = self.get_current_model_version()
        return self.get_model_metadata(version=version)

    def list_model_metadata(self) -> list[dict[str, Any]]:
        versions = self.list_model_versions()
        return [self.get_model_metadata(version=version) for version in versions]

    def list_model_versions(self) -> list[str]:
        prefix = settings.model_minio_root_dir.strip("/") + "/"
        suffixes = {
            "/" + settings.model_filename,
            "/" + settings.model_metrics_filename,
            "/" + settings.model_dataset_filename,
        }

        objects = self.minio_component.client.list_objects(
            bucket_name=self.minio_component.settings.bucket_name,
            prefix=prefix,
            recursive=True,
        )

        versions: set[str] = set()

        for item in objects:
            object_name = item.object_name

            if object_name == settings.build_current_model_version_object_name():
                continue

            if not object_name.startswith(prefix):
                continue

            relative_name = object_name[len(prefix):]

            for suffix in suffixes:
                if relative_name.endswith(suffix):
                    version = relative_name[: -len(suffix)]

                    if version:
                        versions.add(version)

        return sorted(versions)

    def download_metrics_dict(self, *, version: str) -> dict[str, Any]:
        object_name = settings.build_metrics_object_name(version)

        try:
            content = self.minio_component.download_bytes(object_name=object_name)
        except OlmsMinioFileNotFoundError:
            return {}

        try:
            return json.loads(content.decode("utf-8"))
        except json.JSONDecodeError:
            logger.warning("Failed to decode model metrics JSON: %s", object_name)
            return {}

    def _safe_object_exists(self, object_name: str) -> bool:
        try:
            return self.minio_component.object_exists(object_name=object_name)
        except Exception:
            logger.exception("Failed to check object existence: %s", object_name)
            return False

    def _safe_stat_object(self, object_name: str):
        try:
            return self.minio_component.stat_object(object_name=object_name)
        except OlmsMinioFileNotFoundError:
            return None

    def _to_int_or_none(self, value: Any) -> int | None:
        if value is None:
            return None

        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    def _to_float_or_none(self, value: Any) -> float | None:
        if value is None:
            return None

        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def _upload_file(self, *, local_path: Path, object_name: str, content_type: str, file_group: str) -> None:
        logger.info("START ModelArtifactStorage::_upload_file local_path=%s object_name=%s", local_path, object_name)

        self.minio_component.upload_bytes(
            content=local_path.read_bytes(),
            original_filename=local_path.name,
            file_group=file_group,
            content_type=content_type,
            object_name=object_name,
            metadata={"artifact-type": file_group, "original-filename": local_path.name},
        )

        logger.info("END ModelArtifactStorage::_upload_file local_path=%s object_name=%s", local_path, object_name)

    def _build_local_model_path(self, version: str) -> Path:
        normalized_version = settings._normalize_version(version)
        return self.local_tmp_dir / "models" / normalized_version / settings.model_filename