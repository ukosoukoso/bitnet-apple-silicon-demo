# BitNet 1-Bit LLM on Apple Silicon (M4 Pro)

Running Microsoft's BitNet b1.58 2B model on Apple Silicon Mac using **CPU only**.

![BitNet Chat Demo](screenshots/chat-demo.png)

## What This Is

This repo demonstrates running the [BitNet](https://github.com/microsoft/BitNet) 1-bit Large Language Model on Apple Silicon Macs. It includes a **critical fix** for ARM NEON detection that was causing crashes on M-series chips.

## The Problem

The original BitNet/llama.cpp code queries the wrong `sysctl` key for NEON detection on macOS:

```c
// Original (broken on Apple Silicon)
sysctlbyname("hw.optional.AdvSIMD", ...)  // Returns 0 on M4 Pro!
```

This causes `NEON = 0` in system_info, leading to suboptimal code paths or crashes.

## The Fix

```c
// Fixed version
sysctlbyname("hw.optional.arm.AdvSIMD", ...)  // Returns 1 correctly
```

See [`neon-detection-fix.patch`](./neon-detection-fix.patch) for the complete patch.

## Quick Start

### Option A: Docker (One-Click) 🐳

```bash
# Clone this repo
git clone https://github.com/ukosoukoso/bitnet-apple-silicon-demo.git
cd bitnet-apple-silicon-demo

# Run with Docker (builds automatically on first run)
chmod +x run-docker.sh
./run-docker.sh
```

Or with docker-compose:
```bash
docker-compose run --rm bitnet
```

### Option B: Native Installation

### 1. Clone and Setup BitNet

```bash
git clone --recursive https://github.com/microsoft/BitNet.git
cd BitNet
```

### 2. Apply the NEON Fix

```bash
# Apply the patch
cd 3rdparty/llama.cpp
patch -p1 < /path/to/neon-detection-fix.patch
cd ../..
```

### 3. Download Model & Build

```bash
# Download the official pre-quantized model
huggingface-cli download microsoft/BitNet-b1.58-2B-4T-gguf \
  --local-dir models/BitNet-b1.58-2B-4T

# Setup and build
python setup_env.py -md models/BitNet-b1.58-2B-4T -q i2_s
```

### 4. Run Inference

```bash
# Single prompt
./build/bin/llama-cli \
  -m models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf \
  -p "Hello, world!" \
  -n 50 -t 8

# Interactive chat (use chat.py from this repo)
python chat.py
```

## Benchmark Results

Tested on **Apple M4 Pro** (14-core CPU, 48GB RAM):

| Metric | Value |
|--------|-------|
| Model | BitNet b1.58 2B (I2_S quantization) |
| Model Size | 1.10 GiB |
| NEON | Enabled ✅ |
| Threads | 8 |
| Prompt eval | ~170 tokens/sec |
| Generation | ~40-70 tokens/sec |

## Docker: One-Click Setup

The easiest way to run BitNet - no manual setup needed!

```bash
git clone https://github.com/ukosoukoso/bitnet-apple-silicon-demo.git
cd bitnet-apple-silicon-demo
./run-docker.sh
```

> First build takes 5-10 minutes (downloads 1.1GB model + compiles).

## Files in This Repo

- `neon-detection-fix.patch` - The ARM NEON detection fix for Apple Silicon
- `chat.py` - Terminal-based multi-turn chat script
- `Dockerfile` - One-click Docker setup
- `run-docker.sh` - Easy runner script
- `README.md` - This file

## Technical Details

### System Info (After Fix)

```
system_info: NEON = 1 | ARM_FMA = 1 | FP16_VA = 1 | MATMUL_INT8 = 1
```

### Why This Matters

BitNet's 1.58-bit quantization is specifically optimized for CPU inference. Getting NEON working correctly enables the ARM-optimized code paths, making inference actually usable on Mac laptops.

## Credits

- [Microsoft BitNet](https://github.com/microsoft/BitNet) - The original BitNet implementation
- This fix was discovered while getting BitNet running on M4 Pro in January 2026

## License

The patch files follow the same license as the original BitNet project (MIT).
