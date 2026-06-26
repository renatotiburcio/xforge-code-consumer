FROM python:3.13-slim AS base

WORKDIR /app

COPY pyproject.toml ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

COPY src/ ./src/

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

CMD ["uvicorn", "myapp.main:app", "--host", "0.0.0.0", "--port", "8000"]
