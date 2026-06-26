FROM python:3.12
WORKDIR /VKR_landscape_design

RUN apt-get update && apt-get install -y --no-install-recommends \
    gdal-bin \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

COPY jwt-guard /jwt-guard

COPY VKR_landscape_design/requirements.txt /VKR_landscape_design
RUN pip3 install --upgrade pip && \
    pip3 install /jwt-guard && \
    pip3 install -r /VKR_landscape_design/requirements.txt

COPY VKR_landscape_design/alembic.ini /VKR_landscape_design
COPY VKR_landscape_design/alembic /VKR_landscape_design/alembic

COPY VKR_landscape_design/app /VKR_landscape_design/app

ENV PYTHONPATH="/VKR_landscape_design/app:${PYTHONPATH}"

EXPOSE 8000

CMD ["sh", "-c", "\
    cd /VKR_landscape_design && \
    alembic upgrade head && \
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --log-level info \
"]
