FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (Railway uses PORT env var)
EXPOSE 8000

# Run the application (Railway injects PORT env var)
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}

