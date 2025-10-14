# Base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Expose API port
EXPOSE 8000

# Default command
ENV PYTHONPATH=/app
CMD ["python", "-m", "backend.main"]
