FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for PostgreSQL
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything
COPY . .

# CRITICAL: Tell Python to look in the current directory for the 'app' module
ENV PYTHONPATH=/app

EXPOSE 8000

# Bind to 0.0.0.0 so the host machine (your PC) can talk to the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]