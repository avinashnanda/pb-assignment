# Use PyTorch base image with CUDA 12.8 and cuDNN 9
FROM pytorch/pytorch:2.8.0-cuda12.8-cudnn9-runtime

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy project files; make sure .dockerignore excludes large data
COPY . .

# Install additional Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI using Uvicorn with 2 workers
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
