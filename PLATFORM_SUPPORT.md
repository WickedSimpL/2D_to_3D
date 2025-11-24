# Platform Support

The 2D to 3D Converter is designed to work across multiple platforms with optimized support for different hardware accelerators.

## Supported Platforms

| Platform | Status | GPU Acceleration | Notes |
|----------|--------|------------------|-------|
| **macOS (Apple Silicon)** | ✅ Fully Supported | MPS (Metal) | M1/M2/M3/M4 Macs |
| **macOS (Intel)** | ✅ Fully Supported | CPU Only | Works well, slower than Apple Silicon |
| **Linux** | ✅ Fully Supported | CUDA | NVIDIA GPUs recommended |
| **Windows** | ✅ Fully Supported | CUDA | NVIDIA GPUs recommended |

## Hardware Acceleration

### Apple Silicon (M1/M2/M3/M4) - MPS

**Advantages:**
- Native GPU acceleration through Metal Performance Shaders
- Unified memory architecture (GPU shares system RAM)
- Energy efficient
- 2-5x faster than CPU mode

**Considerations:**
- Shares RAM with system (8GB minimum, 16GB recommended)
- May not support all operations (automatic CPU fallback)
- Thermal throttling possible under sustained load

**Setup:**
```bash
# PyTorch automatically includes MPS support
pip install torch torchvision torchaudio
```

### NVIDIA GPUs - CUDA

**Advantages:**
- Fastest performance for deep learning tasks
- Dedicated VRAM
- Full operation support
- Best for production use

**Considerations:**
- Requires NVIDIA GPU with CUDA support
- Separate CUDA installation needed
- Higher power consumption

**Setup:**
```bash
# Install CUDA version appropriate for your GPU
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### CPU Mode

**Advantages:**
- Works on any system
- No special setup required
- Reliable and stable

**Considerations:**
- Significantly slower (5-10x vs GPU)
- Higher power consumption
- Not recommended for batch processing

**Setup:**
```bash
# Standard PyTorch installation defaults to CPU if no GPU found
pip install torch torchvision
```

## Performance Comparison

Based on 512x512 image with depth=8:

| Hardware | Device | Typical Time | Relative Speed |
|----------|--------|--------------|----------------|
| M1 Mac | MPS | 30-60s | 3x |
| M1 Pro/Max | MPS | 20-40s | 4x |
| M2/M3 Mac | MPS | 25-50s | 3x |
| NVIDIA RTX 3060 | CUDA | 15-30s | 5x |
| NVIDIA RTX 4090 | CUDA | 10-20s | 8x |
| Intel i7 CPU | CPU | 2-5min | 1x (baseline) |

*Times are approximate and vary based on image complexity*

## Platform-Specific Setup Guides

### macOS
- **Comprehensive Guide**: [SETUP_MAC.md](SETUP_MAC.md)
- **Quick Setup**: Run `./setup_mac.sh`
- **Key Features**: MPS acceleration, Homebrew integration

### Linux
- **Standard Installation**: Follow main [README.md](README.md)
- **CUDA Setup**: Install NVIDIA drivers and CUDA toolkit
- **Docker**: Container support available

### Windows
- **Standard Installation**: Follow main [README.md](README.md)
- **CUDA Setup**: Install NVIDIA drivers and CUDA toolkit
- **WSL2**: Linux subsystem supported

## System Requirements by Platform

### macOS

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| OS Version | macOS 11.0 | macOS 13.0+ |
| RAM | 8GB | 16GB+ |
| Storage | 10GB | 20GB+ |
| Python | 3.8 | 3.10-3.11 |

### Linux

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Distribution | Ubuntu 20.04 | Ubuntu 22.04+ |
| RAM | 8GB | 16GB+ |
| GPU VRAM | - | 6GB+ (NVIDIA) |
| Storage | 10GB | 20GB+ |
| Python | 3.8 | 3.10-3.11 |

### Windows

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| OS Version | Windows 10 | Windows 11 |
| RAM | 8GB | 16GB+ |
| GPU VRAM | - | 6GB+ (NVIDIA) |
| Storage | 10GB | 20GB+ |
| Python | 3.8 | 3.10-3.11 |

## Device Detection

The application automatically detects the best available device:

1. **CUDA** (if NVIDIA GPU with CUDA support)
2. **MPS** (if Apple Silicon Mac)
3. **CPU** (fallback for all platforms)

You can verify your device by running:

```bash
python test_installation.py
```

Or check programmatically:

```python
import torch

if torch.cuda.is_available():
    print(f"Using CUDA: {torch.cuda.get_device_name(0)}")
elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
    print("Using MPS: Apple Silicon GPU")
else:
    print("Using CPU")
```

## Troubleshooting by Platform

### macOS

**Issue**: MPS out of memory
```bash
# Reduce quality settings
python main.py --image input.jpg --mask mask.png --depth 7
```

**Issue**: Homebrew package conflicts
```bash
# Use virtual environment
python3 -m venv venv
source venv/bin/activate
```

### Linux

**Issue**: CUDA out of memory
```bash
# Clear GPU memory
nvidia-smi
# Kill other GPU processes if needed
```

**Issue**: Missing CUDA libraries
```bash
# Install CUDA toolkit
sudo apt install nvidia-cuda-toolkit
```

### Windows

**Issue**: DLL load failed
```bash
# Install Visual C++ Redistributables
# Download from Microsoft website
```

**Issue**: Path issues
```bash
# Use forward slashes or raw strings
python main.py --image "C:/path/to/image.jpg"
```

## Cross-Platform Compatibility

### File Paths
The application handles platform-specific path separators automatically using Python's `pathlib`.

### Dependencies
All dependencies are cross-platform compatible:
- PyTorch: macOS, Linux, Windows
- Open3D: macOS, Linux, Windows
- Gradio: macOS, Linux, Windows
- Trimesh: macOS, Linux, Windows

### Output Formats
Generated files (.ply, .obj, .stl) are platform-independent and can be transferred between systems.

## Cloud and Remote Options

### Jupyter Notebooks
```bash
pip install jupyter
jupyter notebook
```

### Google Colab
- Free GPU access
- No local installation required
- Limited session time

### Docker
```dockerfile
# Coming soon
# Containerized version for consistent deployment
```

## Performance Optimization by Platform

### macOS
1. Close unnecessary applications to free RAM
2. Enable High Power Mode (M1 Pro/Max/Ultra)
3. Keep Mac plugged in during processing
4. Use depth=7-9 for 8GB Macs, depth=9-10 for 16GB+

### Linux
1. Close other GPU applications
2. Monitor GPU usage: `nvidia-smi`
3. Use CUDA for best performance
4. Consider batch processing for multiple images

### Windows
1. Close other GPU applications
2. Update NVIDIA drivers regularly
3. Use Task Manager to monitor resources
4. Disable Windows visual effects for better performance

## Future Platform Support

### Planned
- AMD GPU support (ROCm)
- Intel GPU support (oneAPI)
- Web browser version (WebGPU)
- Mobile support (iOS/Android)

### Experimental
- Raspberry Pi (CPU only)
- ARM Linux servers
- Cloud functions (AWS Lambda, Google Cloud Functions)

## Getting Help

For platform-specific issues:

1. Check the appropriate setup guide:
   - [SETUP_MAC.md](SETUP_MAC.md) for macOS
   - [README.md](README.md) for Linux/Windows
2. Run diagnostics: `python test_installation.py`
3. Check device detection in application logs
4. Open an issue with platform details

---

**This application is designed to work everywhere you do!** 🚀
