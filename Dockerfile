FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl wget git build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium --with-deps

COPY . .

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "uvicorn", "dashboards.api:app", "--host", "0.0.0.0", "--port", "8080"]
