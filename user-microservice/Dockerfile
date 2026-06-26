FROM python:3.12
WORKDIR /user-microservice

COPY user-microservice/requirements.txt /user-microservice
RUN pip3 install --upgrade pip && \
    pip3 install -r /user-microservice/requirements.txt

COPY jwt-guard /jwt-guard
RUN pip3 install /jwt-guard

COPY user-microservice/alembic.ini /user-microservice
COPY user-microservice/alembic /user-microservice/alembic
COPY user-microservice/app /user-microservice/app
COPY user-microservice/keys /user-microservice/keys

ENV PYTHONPATH="/user-microservice/app:${PYTHONPATH}"

EXPOSE 8010

CMD ["sh", "-c", "\
    cd /user-microservice && \
    alembic upgrade head && \
    uvicorn app.main:app --host 0.0.0.0 --port 8010 --log-level info \
"]
