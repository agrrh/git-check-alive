FROM python:3.10

WORKDIR /app

COPY ./requirements.api.txt ./
RUN pip install -r ./requirements.api.txt

COPY ./ ./

ENV PYTHONUNBUFFERED yes
ENV WEB_CONCURRENCY 2

ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "app_api:app"]
CMD []
