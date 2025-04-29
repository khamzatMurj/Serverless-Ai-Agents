# syntax=docker/dockerfile:1

# 1) Build stage: install dependencies and build wheels
FROM python:3.11-slim AS builder
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install build tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

# 2) Final stage: copy wheels and application code
FROM python:3.11-slim
WORKDIR /app

# Copy compiled wheels and install them
COPY --from=builder /wheels /wheels
COPY requirements.txt .
RUN pip install --no-cache /wheels/*

# Copy application code
COPY . .

# Default command
CMD ["python", "lambda_function.py"]
