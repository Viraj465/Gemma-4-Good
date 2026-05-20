FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    "fastapi>=0.104.1" \
    "uvicorn[standard]>=0.24.0" \
    "sse-starlette>=1.8.2" \
    "pydantic>=2.5.2" \
    "python-dotenv>=1.0.0" \
    "httpx>=0.25.0"

COPY . .

EXPOSE 7860

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
