# Use official Python image
FROM python:3.11-slim

ENV PYTHONUTF8=1

# Install system dependencies and curl for installing poetry
RUN apt-get update && apt-get install -y curl build-essential

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Set working directory
WORKDIR /app

# Copy only the dependency files first (for better Docker caching)
COPY pyproject.toml poetry.lock ./

# Install dependencies using Poetry (without creating a virtual environment)
RUN poetry config virtualenvs.create false && \
    poetry config installer.max-workers 1 && \
    pip config set global.timeout 100 && \
    pip config set global.retries 10 && \
    poetry install --no-root --only main --no-interaction --no-ansi

# Copy the rest of the application code
COPY . .

# Expose FastAPI's port
EXPOSE 8000

# Run FastAPI using Uvicorn
CMD ["uvicorn", "src.wrapstorm.main:app", "--host", "0.0.0.0", "--port", "8000"]
