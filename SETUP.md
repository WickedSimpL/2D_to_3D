# Setup Guide for 2D to 3D Converter

This guide will walk you through setting up the 2D to 3D Converter application.

## Prerequisites

- Python 3.8 or higher
- CUDA-capable GPU (recommended, but not required)
- Git
- 8GB+ RAM
- ~10GB disk space for models and checkpoints

## Step-by-Step Installation

### 1. Create a Virtual Environment

It's recommended to use a virtual environment to avoid dependency conflicts:

```bash
# Using venv
python -m venv venv

# Activate on Linux/Mac
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

Or using conda:

```bash
conda create -n 2d-to-3d python=3.10
conda activate 2d-to-3d
```

### 2. Install PyTorch

Install PyTorch with CUDA support (if you have a GPU):

```bash
# For CUDA 11.8
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# For CUDA 12.1
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# For CPU only
pip install torch torchvision
```

### 3. Install Project Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install SAM 3D Objects

Clone and install the SAM 3D Objects repository:

```bash
# Clone in a separate directory (outside this project)
cd ..
git clone https://github.com/facebookresearch/sam-3d-objects.git
cd sam-3d-objects

# Follow their setup instructions
# Install their requirements
pip install -r requirements.txt
pip install -r requirements.inference.txt
pip install -r requirements.p3d.txt

# Install sam-3d-objects package
pip install -e .
```

### 5. Download Model Checkpoints

```bash
cd /path/to/2D_to_3D

# Create checkpoints directory
mkdir -p checkpoints/sam-3d-objects

# Download model checkpoints
# Method 1: Using wget (Linux/Mac)
cd checkpoints/sam-3d-objects
wget <checkpoint_url>  # Get URL from SAM 3D Objects repository

# Method 2: Using the SAM 3D Objects download script
cd /path/to/sam-3d-objects
python scripts/download_checkpoints.py --output /path/to/2D_to_3D/checkpoints/sam-3d-objects
```

### 6. Optional: Install Segment Anything (for better masking)

For improved mask generation from point selections:

```bash
pip install segment-anything

# Download SAM checkpoint
mkdir -p checkpoints
cd checkpoints
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth
```

### 7. Verify Installation

Test that everything is installed correctly:

```bash
cd /path/to/2D_to_3D
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
python -c "import open3d; print(f'Open3D: {open3d.__version__}')"
python -c "import trimesh; print(f'Trimesh: {trimesh.__version__}')"
python -c "import gradio; print(f'Gradio: {gradio.__version__}')"

# Test SAM 3D Objects import
python -c "from sam_3d_objects.inference import Inference; print('SAM 3D Objects: OK')"
```

## Configuration

### Update Checkpoint Paths

If your checkpoints are in a different location, update the path in your code:

1. Open `src/sam_integration/sam_processor.py`
2. Update the `checkpoint_path` parameter in `__init__`:

```python
def __init__(self, checkpoint_path=None):
    self.checkpoint_path = checkpoint_path or "/path/to/your/checkpoints"
```

### GPU Configuration

By default, the application will use CUDA if available. To force CPU mode:

```python
# In src/sam_integration/sam_processor.py
self.device = "cpu"  # Force CPU mode
```

## Quick Start Test

### Test with GUI

```bash
python main.py --gui
```

The web interface should open at `http://localhost:7860`

### Test with Example Image

If you have an image and mask ready:

```bash
# Create test directory
mkdir -p data/input

# Place your test image and mask in data/input/
# Then run:
python main.py --image data/input/test.jpg --mask data/input/test_mask.png
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'sam_3d_objects'"

**Solution**: Make sure you've installed SAM 3D Objects and it's in your Python path:

```bash
cd /path/to/sam-3d-objects
pip install -e .
```

### Issue: "CUDA out of memory"

**Solution**:
1. Reduce image resolution before processing
2. Use lower Poisson depth: `--depth 7`
3. Use CPU mode if GPU memory is insufficient

### Issue: "FileNotFoundError: Config not found"

**Solution**: Ensure checkpoints are downloaded and the path is correct:

```bash
ls -la checkpoints/sam-3d-objects/
# Should contain: pipeline.yaml and model checkpoint files
```

### Issue: Gradio interface not loading

**Solution**:
1. Check if port 7860 is available
2. Try specifying a different port:

```python
# In src/gui/app.py, modify the launch line:
demo.launch(share=False, server_port=7861)
```

### Issue: Import errors with Open3D

**Solution**: Open3D may have issues with some Python versions. Try:

```bash
pip uninstall open3d
pip install open3d==0.17.0
```

## Performance Tips

1. **Use GPU**: CUDA acceleration significantly speeds up processing
2. **Optimize image size**: Resize large images to 512-1024px for faster processing
3. **Adjust Poisson depth**: Start with depth=7 for testing, increase to 9-10 for final output
4. **Batch processing**: Process multiple objects using the CLI mode with a script

## Next Steps

Once setup is complete:

1. Read the main [README.md](README.md) for usage instructions
2. Try the GUI: `python main.py --gui`
3. Explore the examples in the `examples/` directory
4. Check out the [SAM 3D Objects documentation](https://github.com/facebookresearch/sam-3d-objects)

## Getting Help

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review [SAM 3D Objects Issues](https://github.com/facebookresearch/sam-3d-objects/issues)
3. Open an issue in this repository with:
   - Your Python version
   - Operating system
   - Error message
   - Steps to reproduce

## System Requirements Summary

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Python | 3.8 | 3.10+ |
| RAM | 8GB | 16GB+ |
| GPU | None (CPU mode) | NVIDIA GPU with 8GB+ VRAM |
| Disk Space | 5GB | 10GB+ |
| OS | Windows 10, Ubuntu 20.04, macOS 11+ | Latest versions |
