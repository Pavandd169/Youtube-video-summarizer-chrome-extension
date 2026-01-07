FROM python:3.10-slim

# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies (minimal)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency list first (for Docker cache)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY api ./api
COPY summarizer ./summarizer

# Expose API port
EXPOSE 8000

# 🔑 THIS replaces "uvicorn api.main:app --reload"
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]