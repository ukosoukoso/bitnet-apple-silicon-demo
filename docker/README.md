# BitNet Docker (Experimental)

⚠️ **Status: Work in Progress**

Docker runs Linux ARM64, which has different issues than macOS native.

## Known Issues

- NEON detection works (`NEON = 1`)
- But `MATMUL_INT8 = 0`, `BLAS = 0` - some optimizations not available
- Output may be garbled due to missing optimizations

## If you want to try anyway

```bash
./run-docker.sh
```

## Recommendation

For now, use the **macOS native** version in `../macos/` which is tested and working.
