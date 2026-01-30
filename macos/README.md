# BitNet on macOS (Native)

Run BitNet 1-bit LLM on Apple Silicon Mac natively. **Tested and working on M4 Pro.**

## The Fix

The original BitNet/llama.cpp has a bug in NEON detection on macOS:

```c
// Original (broken) - queries wrong sysctl key
sysctlbyname("hw.optional.AdvSIMD", ...)  // Returns 0 on M1/M2/M3/M4!

// Fixed - use correct key with fallback
sysctlbyname("hw.optional.arm.AdvSIMD", ...)  // Returns 1 correctly
```

## Quick Start

```bash
# 1. Clone BitNet
git clone --recursive https://github.com/microsoft/BitNet.git
cd BitNet

# 2. Apply the NEON fix
cd 3rdparty/llama.cpp
patch -p1 < /path/to/neon-detection-fix.patch
cd ../..

# 3. Download model
huggingface-cli download microsoft/BitNet-b1.58-2B-4T-gguf \
  --local-dir models/BitNet-b1.58-2B-4T

# 4. Build
python setup_env.py -md models/BitNet-b1.58-2B-4T -q i2_s

# 5. Run
./build/bin/llama-cli -m models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf \
  -p "Hello" -n 50 -t 8
```

## Chat Script

Copy `chat.py` to your BitNet directory and run:

```bash
python chat.py
```

## Verified Results

```
system_info: NEON = 1 | ARM_FMA = 1 | FP16_VA = 1 | MATMUL_INT8 = 1 | BLAS = 1
```

Speed: ~40-70 tokens/sec on M4 Pro.
