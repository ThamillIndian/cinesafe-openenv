FROM python:3.11-slim

WORKDIR /app

# Install only pinned runtime dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source after dependencies for better layer caching
COPY . /app/

ENV HOST=0.0.0.0
ENV PORT=7860

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
