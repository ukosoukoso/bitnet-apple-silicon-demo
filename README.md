# BitNet 1-Bit LLM on Apple Silicon

Running Microsoft's BitNet b1.58 2B model on Apple Silicon Mac.

![BitNet Chat Demo](screenshots/chat-demo.png)

## Choose Your Setup

| Setup | Status | Description |
|-------|--------|-------------|
| [**macos/**](./macos/) | ✅ **Working** | Native macOS with NEON fix |
| [**docker/**](./docker/) | ⚠️ Experimental | Docker Linux ARM64 (WIP) |

## TL;DR - macOS Native (Recommended)

```bash
# Clone BitNet and apply the NEON fix
git clone --recursive https://github.com/microsoft/BitNet.git
cd BitNet/3rdparty/llama.cpp
curl -O https://raw.githubusercontent.com/ukosoukoso/bitnet-apple-silicon-demo/main/macos/neon-detection-fix.patch
patch -p1 < neon-detection-fix.patch
cd ../..

# Download model and build
huggingface-cli download microsoft/BitNet-b1.58-2B-4T-gguf --local-dir models/BitNet-b1.58-2B-4T
python setup_env.py -md models/BitNet-b1.58-2B-4T -q i2_s

# Run
./build/bin/llama-cli -m models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf -p "Hello" -n 50 -t 8
```

## The Problem We Fixed

BitNet's llama.cpp fork has a bug in NEON detection on macOS Apple Silicon:

```c
// Original (broken)
sysctlbyname("hw.optional.AdvSIMD", ...)  // Returns 0 on M1/M2/M3/M4!

// Fixed
sysctlbyname("hw.optional.arm.AdvSIMD", ...)  // Returns 1 correctly
```

This caused `NEON = 0` in system_info, leading to crashes or poor performance.

## Benchmark (M4 Pro)

| Metric | Value |
|--------|-------|
| Model | BitNet b1.58 2B (I2_S) |
| Size | 1.10 GiB |
| NEON | ✅ Enabled |
| Speed | ~40-70 tokens/sec |

## Credits

- [Microsoft BitNet](https://github.com/microsoft/BitNet)

## License

MIT (same as BitNet)
