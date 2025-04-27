# Dockerfile

# 1. Use official slim Python image
FROM python:3.10-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy your poetry files
COPY pyproject.toml poetry.lock* /app/

# 4. Install OS-level build deps needed by torch, Pillow, etc.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# 5. Install Poetry 1.5.1 and your Python deps (no dev-deps, no self-install)
RUN pip install --upgrade pip && \
    pip install poetry==1.5.1 && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-root

# 6. Copy your app code
COPY src/ /app/src/

# 7. Expose the Streamlit default port
EXPOSE 8501

# 8. Tell Streamlit to run headless in containers
ENV STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLECORS=false \
    STREAMLIT_SERVER_PORT=8501

# 9. Copy your .env into the image
COPY src/.env /app/.env

# 10. Launch the app
CMD ["streamlit", "run", "src/app.py"]
