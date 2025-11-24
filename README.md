# 2D to 3D Converter

Convert 2D images to 3D watertight meshes using Meta's SAM 3D Objects model. This application provides an intuitive GUI for selecting objects in images and automatically generates high-quality 3D reconstructions.

## Features

- **Interactive GUI**: Simple web-based interface for image upload and coordinate selection
- **SAM 3D Objects Integration**: Leverages Meta's state-of-the-art 3D reconstruction model
- **Point Cloud Generation**: Creates detailed point clouds (.ply) from 2D images
- **Watertight Mesh Conversion**: Converts point clouds to solid, printable 3D meshes
- **Multiple Export Formats**: Supports OBJ, PLY, and STL output formats

## Pipeline Overview

1. **User Input**: Upload an image and click to select the object of interest
2. **Mask Generation**: Creates segmentation mask from selected coordinates
3. **3D Reconstruction**: Uses SAM 3D Objects to generate a point cloud
4. **Mesh Processing**: Converts the point cloud to a watertight mesh using Poisson reconstruction

## Project Structure

```
2D_to_3D/
├── src/
│   ├── gui/                    # Gradio web interface
│   │   └── app.py
│   ├── sam_integration/        # SAM 3D Objects wrapper
│   │   └── sam_processor.py
│   └── mesh_processing/        # Point cloud to mesh conversion
│       └── mesh_converter.py
├── data/
│   ├── input/                  # Input images and masks
│   └── output/                 # Generated point clouds and meshes
├── examples/                   # Example images and outputs
├── main.py                     # Main application entry point
└── requirements.txt            # Python dependencies
```

## Installation

> **🍎 Mac Users**: See [SETUP_MAC.md](SETUP_MAC.md) for Mac-specific installation instructions, including Apple Silicon (M1/M2/M3) support with MPS acceleration.

### 1. Clone the Repository

```bash
git clone https://github.com/WickedSimpL/2D_to_3D.git
cd 2D_to_3D
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install SAM 3D Objects

Follow the official installation guide from Meta:

```bash
# Clone SAM 3D Objects repository
git clone https://github.com/facebookresearch/sam-3d-objects.git
cd sam-3d-objects

# Follow their setup instructions
# See: https://github.com/facebookresearch/sam-3d-objects/blob/main/doc/setup.md
```

### 4. Download Model Checkpoints

Download the SAM 3D Objects model checkpoints and place them in the `checkpoints/` directory:

```bash
mkdir -p checkpoints/sam-3d-objects
# Download checkpoints from the official repository
# Place them in checkpoints/sam-3d-objects/
```

## Usage

### GUI Mode (Recommended)

Launch the interactive web interface:

```bash
python main.py --gui
```

Then:
1. Upload an image
2. Click on the object you want to convert to 3D
3. Click "Generate 3D Model"
4. Download the generated point cloud (.ply) and mesh (.obj)

### Command Line Mode

If you already have an image and mask:

```bash
python main.py --image input.jpg --mask mask.png --output output_dir/
```

Options:
- `--depth`: Poisson reconstruction depth (default: 9, higher = more detail)
- `--format`: Output format: obj, ply, or stl (default: obj)

### Visualization

Visualize an existing mesh:

```bash
python main.py --visualize output/mesh.obj
```

## Advanced Configuration

### Poisson Reconstruction Depth

The `--depth` parameter controls the level of detail in the final mesh:
- **6-8**: Lower detail, faster processing
- **9-10**: Medium detail (recommended)
- **11-12**: High detail, slower processing

### Watertight Mesh Generation

The mesh converter uses multiple techniques to ensure watertightness:
1. Poisson surface reconstruction
2. Hole filling
3. Voxelization (if needed)
4. Laplacian smoothing

## Requirements

- Python 3.8+
- CUDA-capable GPU (recommended for SAM 3D Objects)
- 8GB+ RAM
- SAM 3D Objects model checkpoints

## Dependencies

Key libraries:
- **gradio**: Web-based GUI
- **torch**: Deep learning framework
- **open3d**: 3D data processing
- **trimesh**: Mesh manipulation
- **SAM 3D Objects**: 3D reconstruction model

See `requirements.txt` for complete list.

## Troubleshooting

### SAM 3D Objects Not Found

Make sure you've installed SAM 3D Objects following their official guide:
https://github.com/facebookresearch/sam-3d-objects

### Out of Memory Errors

- Reduce the Poisson reconstruction depth: `--depth 7`
- Use a smaller input image
- Close other GPU applications

### Mesh Not Watertight

Try increasing the Poisson depth:
```bash
python main.py --image input.jpg --mask mask.png --depth 10
```

## Examples

Example images and outputs will be added to the `examples/` directory.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Meta AI Research**: For the SAM 3D Objects model
- **Open3D**: For 3D processing capabilities
- **Gradio**: For the easy-to-use GUI framework

## Citation

If you use this project in your research, please cite the original SAM 3D Objects paper:

```bibtex
@article{sam3d2025,
  title={SAM 3D: 3Dfy Anything in Images},
  author={Meta AI Research},
  year={2025}
}
```

## Resources

- [SAM 3D Objects GitHub](https://github.com/facebookresearch/sam-3d-objects)
- [SAM 3D Objects Paper](https://ai.meta.com/research/publications/sam-3d-3dfy-anything-in-images/)
- [Meta AI Demo](https://aidemos.meta.com/segment-anything/editor/convert-image-to-3d)
