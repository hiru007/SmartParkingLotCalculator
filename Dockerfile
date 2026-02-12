# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy requirements if you have any (unittest is built-in)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt || true

# Copy source code
COPY . .

# Run the tests by default
CMD ["python", "-m", "unittest", "discover", "tests"]