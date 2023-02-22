FROM python:3.10

WORKDIR /app

COPY ./requirements.worker.txt ./
RUN pip install -r ./requirements.worker.txt

COPY ./ ./

ENV PYTHONUNBUFFERED yes
ENV WEB_CONCURRENCY 2

ENTRYPOINT ["python", "app_worker.py"]
CMD []
