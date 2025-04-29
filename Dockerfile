# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY recommendation /app/recommendation
COPY . .

# Set environment variables (adjust as needed)
# ENV PYTHONPATH=/app
# ENV PYTHONUNBUFFERED=1

# Expose port if needed (adjust based on your application)
# EXPOSE 8000

# Entrypoint (adjust based on your main application)
CMD ["python", "lambda_function.py"]
# or
# CMD ["python", "agents/main.py"]
