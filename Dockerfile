FROM python:3.11-slim

WORKDIR /app

# Copy dependency files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application for OpenEnv v0.2.0 compatibility
COPY . /app/
RUN pip install --no-cache-dir .

# Required env bindings for spaces
ENV HOST="0.0.0.0"
ENV PORT=7860

# CMD now uses the root-level server wrapper which matches [project.scripts]
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
