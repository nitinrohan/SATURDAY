FROM node:18-alpine AS frontend-builder

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY src ./src
COPY public ./public
RUN npm run build

FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Copy React build from frontend-builder
COPY --from=frontend-builder /app/build ./BACKEND/build

# Expose port
EXPOSE 10000

# Set environment variables
ENV PYTHONPATH=/app
ENV FLASK_ENV=production

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "--workers", "2", "--timeout", "120", "BACKEND.backend:app"] 