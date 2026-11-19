FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements-all.txt requirements-ui.txt ./
RUN python -m pip install --upgrade pip \
    && pip install -r requirements-all.txt -r requirements-ui.txt

COPY day9/ ./day9/
COPY ui/ ./ui/

EXPOSE 8000 8501
