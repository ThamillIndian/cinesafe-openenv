FROM python:3.11-slim

WORKDIR /app

# Copy dependency files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY cinesafe_openenv/ /app/cinesafe_openenv/
COPY openenv.yaml /app/

# Required env bindings for spaces
ENV HOST="0.0.0.0"
ENV PORT=7860

# We use uvicorn to serve the environment's internal FASTAPI app (if required)
CMD ["uvicorn", "cinesafe_openenv.server.app:app", "--host", "0.0.0.0", "--port", "7860"]
