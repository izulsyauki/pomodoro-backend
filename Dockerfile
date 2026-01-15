# Gunakan image Python yang ringan
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Set environment variables untuk Python
# PYTHONDONTWRITEBYTECODE: Mencegah Python menulis file .pyc
# PYTHONUNBUFFERED: Memastikan output logs langsung keluar
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies sistem yang mungkin dibutuhkan
# libpq-dev dan gcc dibutuhkan untuk psycopg2 (driver database)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt dan install dependencies Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy seluruh source code ke dalam image
COPY . .

# Expose port yang digunakan aplikasi
EXPOSE 8001

# Command default untuk menjalankan aplikasi
# Kita menggunakan sh -c untuk bisa chaining command jika nanti butuh migrasi
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8001"]
