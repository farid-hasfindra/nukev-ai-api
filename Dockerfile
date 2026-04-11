FROM python:3.11-slim

WORKDIR /app

# Install dependencies yang dibutuhkan sistem (build-essential untuk beberapa paket python)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements dan install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh source code
COPY . .

# Tambahkan path aplikasi ke PYTHONPATH
ENV PYTHONPATH=/app

# Expose port 7860 (Standar Hugging Face Spaces)
EXPOSE 7860

# Jalankan aplikasi dengan uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
