FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for playwright and lxml
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Create a non-root user for security
RUN adduser --system --uid 1001 backenduser \
    && chown -R backenduser /app

# Switch to the non-root user
USER backenduser

# Railway sets PORT dynamically
ENV PORT=8000
EXPOSE ${PORT}

# Start FastAPI server using the PORT env var
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
