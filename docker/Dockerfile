# BitNet 1-bit LLM Docker Image
# Supports: linux/arm64 (Apple Silicon via Docker Desktop, AWS Graviton, etc.)
# Also supports: linux/amd64 (Intel/AMD)

FROM python:3.11-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    git \
    cmake \
    build-essential \
    clang \
    && rm -rf /var/lib/apt/lists/*

# Clone BitNet
WORKDIR /app
RUN git clone --recursive https://github.com/microsoft/BitNet.git

# Apply NEON detection fix for Linux ARM64
WORKDIR /app/BitNet/3rdparty/llama.cpp
COPY neon-detection-fix.patch /tmp/
RUN patch -p1 < /tmp/neon-detection-fix.patch || true

# Build BitNet
WORKDIR /app/BitNet
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir huggingface_hub

# Download model and build
RUN python -c "from huggingface_hub import snapshot_download; snapshot_download('microsoft/BitNet-b1.58-2B-4T-gguf', local_dir='models/BitNet-b1.58-2B-4T')"
RUN python setup_env.py -md models/BitNet-b1.58-2B-4T -q i2_s

# Runtime image
FROM python:3.11-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy built artifacts
WORKDIR /app
COPY --from=builder /app/BitNet/build /app/build
COPY --from=builder /app/BitNet/models /app/models
COPY chat.py /app/

# Set environment - include library path for llama.so
ENV PYTHONUNBUFFERED=1
ENV LD_LIBRARY_PATH=/app/build/3rdparty/llama.cpp/src:/app/build/3rdparty/llama.cpp/ggml/src:/app/build/lib:/app/build/bin:$LD_LIBRARY_PATH

# Default command - Terminal chat
CMD ["python", "chat.py"]
