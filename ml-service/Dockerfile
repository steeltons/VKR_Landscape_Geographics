FROM python:3.12
WORKDIR /ml-service

# Устанавливаем системные зависимости для geopandas, shapely, pyproj
RUN apt-get update && apt-get install -y --no-install-recommends \
    gdal-bin \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем локальную зависимость olms-minio-component
COPY ./olms-minio-component /olms-minio-component

COPY ml-service/requirements.txt /ml-service
RUN pip3 install --upgrade pip && \
    pip3 install /olms-minio-component && \
    grep -v "olms-minio-component" /ml-service/requirements.txt | pip3 install -r /dev/stdin

COPY ml-service/alembic.ini /ml-service
COPY ml-service/alembic /ml-service/alembic
COPY ml-service/app /ml-service/app

ENV PYTHONPATH="/ml-service/app:${PYTHONPATH}"

EXPOSE 8030

CMD ["sh", "-c", "\
    cd /ml-service && \
    alembic upgrade head && \
    uvicorn app.main:app --host 0.0.0.0 --port ${APP_PORT:-8030} --log-level info \
"]
