FROM python:3.9-slim

WORKDIR /app

RUN useradd -m appuser

RUN chown -R appuser:appuser /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER appuser

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
