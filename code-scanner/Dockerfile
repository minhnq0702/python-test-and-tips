# Multi-architecture support for ARM and x86
FROM python:3.11-slim

# Install zbar library and dependencies for both architectures
RUN apt-get update && apt-get install -y \
    libzbar0 \
    libzbar-dev \
    # libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .
COPY image.jpg .

# Run the application
CMD ["python", "main.py"]
