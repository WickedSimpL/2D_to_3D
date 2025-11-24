# Mac Setup Guide for 2D to 3D Converter

This guide covers installation and setup on macOS, including Apple Silicon (M1/M2/M3) Macs.

## System Requirements

### Minimum
- macOS 11.0 (Big Sur) or later
- 8GB RAM
- 10GB free disk space
- Python 3.8+

### Recommended for Best Performance
- macOS 13.0 (Ventura) or later
- Apple Silicon Mac (M1/M2/M3/M4) for MPS acceleration
- 16GB+ RAM
- 20GB free disk space
- Python 3.10 or 3.11

## Installation Steps

### 1. Install Homebrew (if not already installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install Python

```bash
# Install Python 3.11 (recommended)
brew install python@3.11

# Verify installation
python3 --version
```

### 3. Clone the Repository

```bash
git clone https://github.com/WickedSimpL/2D_to_3D.git
cd 2D_to_3D
```

### 4. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 5. Install PyTorch for Mac

#### For Apple Silicon (M1/M2/M3/M4):

```bash
# Install PyTorch with MPS (Metal Performance Shaders) support
pip install torch torchvision torchaudio
```

This will automatically install the appropriate version with MPS support for GPU acceleration on Apple Silicon.

#### For Intel Macs:

```bash
# Install PyTorch (CPU only)
pip install torch torchvision torchaudio
```

### 6. Install Project Dependencies

```bash
pip install -r requirements.txt
```

**Mac-specific notes:**
- Open3D installation may take a few minutes on Mac
- Some packages may need to compile from source on Apple Silicon

### 7. Install SAM 3D Objects

```bash
# Clone SAM 3D Objects (outside project directory)
cd ..
git clone https://github.com/facebookresearch/sam-3d-objects.git
cd sam-3d-objects

# Install dependencies
pip install -r requirements.txt
pip install -r requirements.inference.txt
pip install -r requirements.p3d.txt

# Install the package
pip install -e .

# Return to project directory
cd ../2D_to_3D
```

### 8. Download Model Checkpoints

```bash
# Create checkpoints directory
mkdir -p checkpoints/sam-3d-objects

# Download checkpoints from SAM 3D Objects repository
# Follow their instructions at:
# https://github.com/facebookresearch/sam-3d-objects
```

### 9. Verify Installation

```bash
python test_installation.py
```

Expected output:
```
✓ NumPy                      - x.xx.x
✓ Pillow                     - x.xx.x
✓ PyTorch                    - x.xx.x
✓ TorchVision                - x.xx.x
✓ Gradio                     - x.xx.x
✓ OpenCV                     - x.xx.x
✓ Open3D                     - x.xx.x
✓ Trimesh                    - x.xx.x
✓ SciPy                      - x.xx.x
✓ scikit-learn               - x.xx.x
✓ SAM 3D Objects             - Installed
✓ MPS available              - Apple M1/M2/M3 (or "CUDA not available - Will use CPU")
```

## Mac-Specific Considerations

### Apple Silicon (M1/M2/M3) GPU Acceleration

The application automatically detects and uses MPS (Metal Performance Shaders) for GPU acceleration on Apple Silicon Macs:

- **MPS Support**: Significantly faster than CPU (2-5x speedup)
- **Memory**: Unified memory architecture shares RAM with GPU
- **Thermal Management**: May throttle under heavy load

### Performance Expectations

| Mac Type | Device | Expected Speed | Notes |
|----------|--------|----------------|-------|
| M1/M2/M3 Mac | MPS | Fast | GPU accelerated |
| M1 Pro/Max/Ultra | MPS | Very Fast | More GPU cores |
| Intel Mac | CPU | Slower | No GPU acceleration |

### Memory Considerations

On Apple Silicon, the GPU shares memory with system RAM:
- 8GB RAM: Use lower quality settings (depth 6-7)
- 16GB RAM: Standard quality (depth 8-9)
- 32GB+ RAM: High quality (depth 10-11)

## Running the Application

### Launch GUI

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Launch application
python main.py --gui
```

The web interface will open at: `http://localhost:7860`

### Command Line Usage

```bash
# Basic conversion
python main.py --image input.jpg --mask mask.png

# With custom depth (adjust based on your RAM)
python main.py --image input.jpg --mask mask.png --depth 8
```

## Troubleshooting

### Issue: "No module named 'torch'"

**Solution**: Make sure you've activated the virtual environment:
```bash
source venv/bin/activate
pip install torch torchvision
```

### Issue: "MPS backend out of memory"

**Solution**: Apple Silicon shares RAM with GPU. Close other apps or reduce quality:
```bash
python main.py --image input.jpg --mask mask.png --depth 7
```

### Issue: Open3D installation fails on Apple Silicon

**Solution**: Install from conda-forge:
```bash
conda install -c conda-forge open3d
```

Or use wheel file:
```bash
pip install --upgrade pip
pip install open3d
```

### Issue: "xcrun: error: invalid active developer path"

**Solution**: Install Xcode Command Line Tools:
```bash
xcode-select --install
```

### Issue: SSL Certificate errors when downloading

**Solution**:
```bash
pip install --upgrade certifi
/Applications/Python\ 3.11/Install\ Certificates.command  # Adjust Python version
```

### Issue: Gradio interface not accessible

**Solution**: Check firewall settings:
1. System Preferences → Security & Privacy → Firewall
2. Allow Python to accept incoming connections

Or use different port:
```python
# In src/gui/app.py
demo.launch(share=False, server_port=7861)
```

### Issue: "RuntimeError: MPS does not support" error

**Solution**: Some operations may not be supported on MPS. The code will automatically fall back to CPU for those operations. If you continue to have issues:
```python
# Force CPU mode in src/sam_integration/sam_processor.py
self.device = "cpu"
```

## Optimizing for Mac Performance

### 1. Close Unnecessary Applications

Free up RAM and CPU for better performance:
```bash
# Check memory usage
top -l 1 | head -n 10
```

### 2. Adjust Quality Settings

For 8GB Macs:
```bash
python main.py --image input.jpg --mask mask.png --depth 7 --format obj
```

For 16GB+ Macs:
```bash
python main.py --image input.jpg --mask mask.png --depth 9 --format obj
```

### 3. Use Activity Monitor

Monitor performance during processing:
1. Open Activity Monitor (Cmd+Space → "Activity Monitor")
2. Watch CPU and Memory tabs
3. Adjust quality if system struggles

### 4. Enable High Power Mode (M1 Pro/Max/Ultra)

For laptops with High Power Mode:
1. System Preferences → Battery
2. Enable "High Power Mode"
3. Keep Mac plugged in during processing

## Development on Mac

### Using VS Code

```bash
# Install VS Code from: https://code.visualstudio.com/
# Open project
code .

# Install Python extension in VS Code
# Select Python interpreter from venv
```

### Using PyCharm

```bash
# Download PyCharm from: https://www.jetbrains.com/pycharm/
# Open project
# Configure interpreter: venv/bin/python
```

### Jupyter Notebook Support

```bash
pip install jupyter
jupyter notebook
```

## Additional Mac Tools

### Mesh Viewers for Mac

- **MeshLab**: `brew install --cask meshlab`
- **Blender**: `brew install --cask blender`
- **Preview**: Built-in (limited 3D support)

### Viewing Generated Models

```bash
# Open with MeshLab
open -a MeshLab data/output/mesh.obj

# Open with Blender
open -a Blender data/output/mesh.obj
```

## Updating the Application

```bash
# Activate virtual environment
source venv/bin/activate

# Pull latest changes
git pull

# Update dependencies
pip install -r requirements.txt --upgrade
```

## Uninstalling

```bash
# Remove virtual environment
rm -rf venv

# Remove checkpoints (large files)
rm -rf checkpoints

# Remove output files
rm -rf data/output/*

# Remove the entire project
cd ..
rm -rf 2D_to_3D
```

## Performance Benchmarks (Approximate)

Based on typical usage with 512x512 input image:

| Mac Model | Device | Processing Time | Quality Setting |
|-----------|--------|-----------------|-----------------|
| M1 Mac | MPS | 30-60s | depth=8 |
| M1 Pro | MPS | 20-40s | depth=9 |
| M1 Max | MPS | 15-30s | depth=9 |
| M2 Mac | MPS | 25-50s | depth=8 |
| Intel i7 | CPU | 2-5min | depth=7 |

*Times vary based on image complexity and system load*

## Getting Help

If you encounter Mac-specific issues:

1. Check this guide's [Troubleshooting](#troubleshooting) section
2. Verify installation: `python test_installation.py`
3. Check SAM 3D Objects Mac support: https://github.com/facebookresearch/sam-3d-objects/issues
4. Open an issue with:
   - Mac model and OS version
   - Output of `python test_installation.py`
   - Error message
   - Steps to reproduce

## Next Steps

Once setup is complete:

1. ✓ Installation verified
2. → Read [QUICKSTART.md](QUICKSTART.md) for first run
3. → Try the GUI: `python main.py --gui`
4. → Explore examples: `examples/example_usage.py`

---

**Ready to start creating 3D models on your Mac!** 🚀
