# Multi-stage build for Abraham-AI
FROM python:3.9-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip
RUN pip install --upgrade pip setuptools wheel

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ----------------------------------------
# Runtime stage
FROM python:3.9-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create non-root user
RUN useradd --create-home --shell /bin/bash abraham
USER abraham
WORKDIR /home/abraham/app

# Copy application code
COPY --chown=abraham:abraham . .

# Create necessary directories
RUN mkdir -p \
    data/wisdom/jewish \
    data/wisdom/chinese \
    data/models \
    logs

# Download sample wisdom data
RUN curl -L https://raw.githubusercontent.com/Sefaria/Sefaria-Export/master/json/Tanakh/Torah/Genesis/1.json \
    -o data/wisdom/jewish/genesis.json --create-dirs 2>/dev/null || true

# Expose ports
EXPOSE 8000 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["python", "main.py"]