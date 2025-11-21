#!/usr/bin/env python3
"""
Example usage of the 2D to 3D converter modules
This script demonstrates how to use the API programmatically
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sam_integration.sam_processor import SAMProcessor
from mesh_processing.mesh_converter import MeshConverter
from PIL import Image
import numpy as np


def example_1_basic_conversion():
    """
    Example 1: Basic conversion from image to watertight mesh
    """
    print("=" * 60)
    print("Example 1: Basic Image to 3D Mesh Conversion")
    print("=" * 60)

    # Initialize processors
    sam_processor = SAMProcessor()
    mesh_converter = MeshConverter()

    # Load your image
    image_path = "path/to/your/image.jpg"
    image = Image.open(image_path)

    # Define points where you clicked on the image
    # These are (x, y) coordinates
    selected_points = [
        (200, 150),  # First click
        (250, 180),  # Second click
        (300, 200),  # Third click
    ]

    # Generate mask from points
    print("\nGenerating mask from selected points...")
    mask = sam_processor.generate_mask(image, selected_points)

    # Generate point cloud using SAM 3D Objects
    print("Running SAM 3D Objects inference...")
    ply_path = sam_processor.generate_point_cloud(
        image=image,
        mask=mask,
        output_dir="output",
        seed=42
    )
    print(f"✓ Point cloud saved: {ply_path}")

    # Convert to watertight mesh
    print("\nConverting to watertight mesh...")
    mesh_path = mesh_converter.convert_to_watertight_mesh(
        ply_path=ply_path,
        output_dir="output",
        depth=9,
        output_format="obj"
    )
    print(f"✓ Watertight mesh saved: {mesh_path}")

    return ply_path, mesh_path


def example_2_with_existing_mask():
    """
    Example 2: Use pre-existing mask for conversion
    """
    print("\n" + "=" * 60)
    print("Example 2: Conversion with Pre-existing Mask")
    print("=" * 60)

    # Initialize processors
    sam_processor = SAMProcessor()
    mesh_converter = MeshConverter()

    # Load image and mask
    image = sam_processor.load_image("path/to/image.jpg")
    mask = sam_processor.load_mask("path/to/mask.png")

    # Generate point cloud
    print("\nGenerating point cloud...")
    ply_path = sam_processor.generate_point_cloud(
        image=image,
        mask=mask,
        output_dir="output"
    )

    # Convert with higher detail
    print("Converting to high-detail mesh...")
    mesh_path = mesh_converter.convert_to_watertight_mesh(
        ply_path=ply_path,
        depth=10,  # Higher detail
        output_format="stl"  # STL for 3D printing
    )

    return ply_path, mesh_path


def example_3_batch_processing():
    """
    Example 3: Batch process multiple images
    """
    print("\n" + "=" * 60)
    print("Example 3: Batch Processing Multiple Images")
    print("=" * 60)

    sam_processor = SAMProcessor()
    mesh_converter = MeshConverter()

    # List of images to process
    images_and_masks = [
        ("image1.jpg", "mask1.png"),
        ("image2.jpg", "mask2.png"),
        ("image3.jpg", "mask3.png"),
    ]

    results = []

    for i, (img_path, mask_path) in enumerate(images_and_masks, 1):
        print(f"\nProcessing image {i}/{len(images_and_masks)}...")

        try:
            # Load
            image = sam_processor.load_image(img_path)
            mask = sam_processor.load_mask(mask_path)

            # Generate point cloud
            ply_path = sam_processor.generate_point_cloud(
                image, mask, output_dir=f"output/batch_{i}", seed=i
            )

            # Convert to mesh
            mesh_path = mesh_converter.convert_to_watertight_mesh(
                ply_path, output_dir=f"output/batch_{i}"
            )

            results.append((img_path, ply_path, mesh_path))
            print(f"✓ Completed: {img_path}")

        except Exception as e:
            print(f"✗ Failed: {img_path} - {e}")
            continue

    print(f"\nBatch processing complete: {len(results)}/{len(images_and_masks)} successful")
    return results


def example_4_advanced_mesh_processing():
    """
    Example 4: Advanced mesh processing with custom parameters
    """
    print("\n" + "=" * 60)
    print("Example 4: Advanced Mesh Processing")
    print("=" * 60)

    mesh_converter = MeshConverter()

    # Load existing point cloud
    ply_path = "path/to/pointcloud.ply"
    pcd = mesh_converter.load_point_cloud(ply_path)

    # Estimate normals
    print("Estimating normals...")
    pcd = mesh_converter.estimate_normals(pcd)

    # Poisson reconstruction with custom parameters
    print("Running Poisson reconstruction...")
    mesh, densities = mesh_converter.poisson_reconstruction(
        pcd,
        depth=11,  # Very high detail
        scale=1.2,
        linear_fit=True
    )

    # Clean mesh aggressively
    print("Cleaning mesh...")
    mesh = mesh_converter.clean_mesh(
        mesh,
        densities=densities,
        density_threshold=0.02  # More aggressive cleaning
    )

    # Make watertight
    print("Making mesh watertight...")
    tri_mesh = mesh_converter.make_watertight(mesh, resolution=30000)

    # Save in multiple formats
    print("Exporting mesh...")
    obj_path = mesh_converter.save_mesh(tri_mesh, "output/model.obj", "obj")
    stl_path = mesh_converter.save_mesh(tri_mesh, "output/model.stl", "stl")
    ply_path = mesh_converter.save_mesh(tri_mesh, "output/model.ply", "ply")

    print(f"✓ Saved in multiple formats:")
    print(f"  - OBJ: {obj_path}")
    print(f"  - STL: {stl_path}")
    print(f"  - PLY: {ply_path}")

    return obj_path, stl_path, ply_path


def example_5_visualize_results():
    """
    Example 5: Visualize generated mesh
    """
    print("\n" + "=" * 60)
    print("Example 5: Visualize Mesh")
    print("=" * 60)

    mesh_converter = MeshConverter()

    mesh_path = "path/to/mesh.obj"

    print(f"Opening mesh viewer for: {mesh_path}")
    print("Close the viewer window to continue...")

    mesh_converter.visualize_mesh(mesh_path)

    print("✓ Visualization closed")


def main():
    """
    Run all examples (modify as needed)
    """
    print("2D to 3D Converter - Example Usage\n")

    # Uncomment the examples you want to run:

    # Example 1: Basic conversion
    # example_1_basic_conversion()

    # Example 2: With existing mask
    # example_2_with_existing_mask()

    # Example 3: Batch processing
    # example_3_batch_processing()

    # Example 4: Advanced processing
    # example_4_advanced_mesh_processing()

    # Example 5: Visualization
    # example_5_visualize_results()

    print("\n" + "=" * 60)
    print("Examples complete!")
    print("=" * 60)
    print("\nTo use these examples:")
    print("1. Update the file paths to your actual images")
    print("2. Uncomment the example you want to run")
    print("3. Run: python examples/example_usage.py")


if __name__ == "__main__":
    main()
