# ---- Stage 1: Builder ----
FROM python:3.9-slim AS builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---- Stage 2: Production ----
FROM python:3.9-slim AS production

# Security: run as non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup -d /app -s /sbin/nologin appuser

WORKDIR /app

# Copy installed dependencies from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY app.py .
COPY gunicorn.conf.py .

# Set ownership
RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Run with Gunicorn (production WSGI server)
CMD ["gunicorn", "--config", "gunicorn.conf.py", "app:app"]
