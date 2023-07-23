FROM python:3.11.4-alpine3.18

WORKDIR /app

ADD . /app

CMD ["python", "-u", "/app/main.py"]