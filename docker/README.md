# BitNet Docker (Linux Servers)

Run BitNet 1-bit LLM in Docker on **Linux servers**.

## Supported Platforms

| Platform | Status |
|----------|--------|
| Linux ARM64 (AWS Graviton, etc.) | ✅ Works |
| Linux x86_64 | ✅ Works |
| Mac Docker Desktop | ❌ Too slow (use `../macos/` instead) |

## Quick Start

```bash
# Build
docker build -t bitnet-1bit .

# Run chat
docker run -it --rm bitnet-1bit

# Or run single prompt
docker run --rm bitnet-1bit ./build/bin/llama-cli \
  -m models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf \
  -p "Hello" -n 50 -t 8
```

## Note for Mac Users

Docker Desktop on Mac uses virtualization which makes LLM inference extremely slow.
**Use the native macOS setup in `../macos/` instead** - it's much faster.
