# Quick Start Guide

Get up and running with the 2D to 3D Converter in under 10 minutes!

## Prerequisites Check

- [ ] Python 3.8 or higher installed
- [ ] GPU with CUDA support (optional but recommended)
- [ ] At least 8GB RAM
- [ ] 10GB free disk space

## Installation (5 minutes)

### Step 1: Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install PyTorch (with CUDA if available)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Install project requirements
pip install -r requirements.txt
```

### Step 2: Install SAM 3D Objects

```bash
# Clone SAM 3D Objects in a separate location
cd ..
git clone https://github.com/facebookresearch/sam-3d-objects.git
cd sam-3d-objects

# Install SAM 3D Objects
pip install -e .

# Return to project directory
cd ../2D_to_3D
```

### Step 3: Download Checkpoints

```bash
# Create checkpoints directory
mkdir -p checkpoints/sam-3d-objects

# Download checkpoints from SAM 3D Objects repository
# Follow instructions at: https://github.com/facebookresearch/sam-3d-objects
```

### Step 4: Verify Installation

```bash
python test_installation.py
```

You should see all checks pass with ✓ marks.

## First Run (2 minutes)

### Launch the GUI

```bash
python main.py --gui
```

This will start a web interface at `http://localhost:7860`

### Using the Interface

1. **Upload Image**: Click the upload area and select an image
2. **Select Object**: Click on the object you want to convert to 3D
   - You can click multiple times to define the object region
   - Use "Clear Points" to start over
3. **Generate**: Click "Generate 3D Model" button
4. **Download**: Download the generated `.ply` and `.obj` files

## Example Workflow

Here's a complete example from start to finish:

```bash
# 1. Prepare your image
# Place an image in data/input/my_image.jpg

# 2. Launch GUI
python main.py --gui

# 3. In the web interface:
#    - Upload data/input/my_image.jpg
#    - Click on the object (e.g., a cup, person, or furniture)
#    - Click "Generate 3D Model"
#    - Wait for processing (may take 1-5 minutes)
#    - Download the generated files from data/output/

# 4. View your 3D model
# Open the .obj file in any 3D viewer like:
#    - Blender
#    - MeshLab
#    - Windows 3D Viewer
#    - Online viewers like threejs.org/editor
```

## Command Line Usage

If you already have a mask:

```bash
python main.py --image data/input/image.jpg --mask data/input/mask.png
```

View generated mesh:

```bash
python main.py --visualize data/output/mesh.obj
```

## Troubleshooting

### "Module not found" errors

```bash
pip install -r requirements.txt
```

### "SAM 3D Objects not installed"

Follow the installation instructions in SETUP.md

### Out of memory

```bash
# Use lower detail setting
python main.py --image input.jpg --mask mask.png --depth 7
```

### GUI not loading

Check if port 7860 is available, or specify different port in `src/gui/app.py`

## What's Next?

- Read [README.md](README.md) for detailed information
- Check [SETUP.md](SETUP.md) for advanced configuration
- Explore [examples/example_usage.py](examples/example_usage.py) for API usage
- Visit [SAM 3D Objects repository](https://github.com/facebookresearch/sam-3d-objects) for more details

## Getting Help

If you run into issues:

1. Check the error message carefully
2. Review the [Troubleshooting section in README.md](README.md#troubleshooting)
3. Ensure all dependencies are installed: `python test_installation.py`
4. Check that checkpoints are downloaded correctly

## Tips for Best Results

1. **Image Quality**: Use high-resolution images with good lighting
2. **Object Selection**: Click on the center and edges of the object
3. **Processing Time**: First run may take longer due to model initialization
4. **Mesh Detail**: Start with default depth (9), increase for more detail
5. **3D Printing**: Use STL format for best compatibility

---

**Ready to create your first 3D model?**

Run `python main.py --gui` and start converting! 🚀
