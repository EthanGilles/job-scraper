FROM python:3.12-slim

WORKDIR /app

COPY backend/requirements.txt backend/requirements.txt
RUN python -m venv venv \
    && ./venv/bin/pip install --no-cache-dir -r backend/requirements.txt

COPY backend/ backend/
RUN mkdir -p /app/data/logs

EXPOSE 8000
CMD ["./venv/bin/python", "-m", "backend.main"]

