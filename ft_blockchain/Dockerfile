FROM python:3.11-slim
LABEL authors="<mariza@student.42malaga.com>, <jpostigo@student.42malaga.com>"
RUN set -ex && apt update && mkdir /app
WORKDIR /app
COPY requirements.txt /app
COPY blkapp.py /app
COPY blockchain.py /app
RUN python -m pip --no-cache-dir install -r requirements.txt

ARG PORT=8000
EXPOSE ${PORT}
CMD uvicorn blkapp:app --host 0.0.0.0 --port ${PORT} --reload ; sh