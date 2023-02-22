FROM python:3.10

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install -r ./requirements.txt

COPY ./ ./

ENV PYTHONUNBUFFERED yes

ENTRYPOINT ["python", "cli.py"]
CMD ["--help"]
