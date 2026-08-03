FROM python:3.11-slim

# Install system dependencies including libxcb
RUN apt-get update && apt-get install -y \
    libxcb1 \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create uploads folder
RUN mkdir -p static/uploads

# Start the app
CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:8080"]