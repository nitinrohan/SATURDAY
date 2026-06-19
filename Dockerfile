FROM python:3.11-slim

WORKDIR /app

COPY requirements-prod.txt .
RUN pip install --no-cache-dir -r requirements-prod.txt

COPY BACKEND/ ./BACKEND/

EXPOSE ${PORT:-8000}

CMD ["gunicorn", "backend:app", "--chdir", "BACKEND", "--bind", "0.0.0.0:${PORT:-8000}"]
