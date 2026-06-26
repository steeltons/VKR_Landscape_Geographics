FROM python:3.12
WORKDIR /gateway

# Копируем локальную зависимость olms-minio-component и скачиваем остальные
COPY ./olms-minio-component /olms-minio-component

COPY gateway/requirements.txt /gateway
RUN pip3 install --upgrade pip && \
    pip3 install /olms-minio-component && \
    grep -v "olms-minio-component" /gateway/requirements.txt | pip3 install -r /dev/stdin
COPY gateway/app /gateway/app

ENV PYTHONPATH="/gateway/app:${PYTHONPATH}"

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--log-level", "info"]
