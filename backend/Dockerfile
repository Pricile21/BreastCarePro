FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install pip upgrade first
RUN pip install --upgrade pip setuptools wheel

# Install Python dependencies with increased timeout for slow connections
# Multi-stage: small packages first, then heavy ML packages
RUN pip install --no-cache-dir \
    fastapi==0.104.1 \
    uvicorn[standard]==0.24.0 \
    python-multipart==0.0.6 \
    sqlalchemy==2.0.23 \
    alembic==1.12.1 \
    psycopg2-binary==2.9.9 \
    python-jose[cryptography]==3.3.0 \
    passlib[bcrypt]==1.7.4 \
    python-dotenv==1.0.0 \
    pydantic-settings==2.1.0 \
    email-validator==2.1.0 \
    structlog==23.2.0 \
    reportlab==4.0.7 \
    aiofiles==23.2.1 \
    httpx==0.25.2 \
    requests==2.31.0 \
    pandas==2.0.3 \
    numpy==1.24.3 \
    matplotlib==3.7.2 \
    seaborn==0.12.2 \
    pytest==7.4.3 \
    pytest-asyncio==0.21.1 \
    black==23.11.0 \
    flake8==6.1.0 \
    mypy==1.7.0

# Install heavy ML packages with longer timeout
RUN pip install --no-cache-dir --default-timeout=1000 tensorflow==2.15.0 && \
    pip install --no-cache-dir --default-timeout=1000 torch==2.1.0 torchvision==0.16.0 && \
    pip install --no-cache-dir --default-timeout=1000 transformers==4.40.0 && \
    pip install --no-cache-dir sentencepiece==0.2.1 protobuf==4.21.12 && \
    pip install --no-cache-dir scikit-learn==1.3.2 opencv-python-headless==4.8.1.78 Pillow==10.1.0

# Copy application code
COPY . .

# Copy articles directory to /articles (for Render deployment)
# Articles are now in backend/articles, so they'll be copied with COPY . .
RUN if [ -d "articles" ]; then cp -r articles /articles; fi || mkdir -p /articles

# Create data directory for uploads
RUN mkdir -p /app/data /app/uploads /app/static

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Run the application
# --limit-max-requests: Augmenter la limite de taille de requête à 100MB (100 * 1024 * 1024 = 104857600 bytes)
# --timeout-keep-alive: Augmenter le timeout pour les requêtes longues (analyses ML)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--limit-concurrency", "1000", "--timeout-keep-alive", "300"]

