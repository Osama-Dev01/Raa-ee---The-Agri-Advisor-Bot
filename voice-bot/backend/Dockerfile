# ✅ Small, clean Python image
FROM python:3.10-slim

# Install system deps for pydub and audio processing
RUN apt-get update && apt-get install -y ffmpeg libsndfile1 && apt-get clean

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install dependencies efficiently
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY backend/ .

# Expose Railway port
EXPOSE 8080

# Run Flask app
CMD ["python", "app.py"]
