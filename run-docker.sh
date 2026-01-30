#!/bin/bash
# One-click BitNet runner

set -e

echo "🚀 BitNet 1-bit LLM Docker Runner"
echo "================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

# Build if image doesn't exist
if ! docker image inspect bitnet-1bit:latest > /dev/null 2>&1; then
    echo "📦 Building BitNet image (this may take 5-10 minutes)..."
    echo "   - Cloning BitNet repo"
    echo "   - Downloading 1.1GB model"
    echo "   - Compiling for ARM64"
    echo ""
    docker build -t bitnet-1bit:latest .
fi

echo "💬 Starting BitNet Chat..."
echo ""
docker run -it --rm bitnet-1bit:latest
