# ============================================================
# ADVANCED Dockerfile — Multi-stage build
#
# ⚠️  Build context = thư mục production/ (thư mục chứa file này)
#     cd 02-docker/production
#     docker build -t my-agent:advanced .
#
#     Railway/Render: set Root Directory = 02-docker/production
# ============================================================

# ──────────────────────────────────────────────────────────
# STAGE 1: Builder
# ──────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt


# ──────────────────────────────────────────────────────────
# STAGE 2: Runtime
# ──────────────────────────────────────────────────────────
FROM python:3.11-slim AS runtime

RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

COPY --from=builder /root/.local /home/appuser/.local
COPY main.py .
COPY utils/mock_llm.py utils/mock_llm.py

RUN chown -R appuser:appuser /app

USER appuser

ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONPATH=/app
ENV PORT=8000

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Shell form để Railway/Render expand $PORT
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 2
