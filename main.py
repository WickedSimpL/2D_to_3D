#!/usr/bin/env python3
"""
Main entry point for the 2D to 3D conversion application
"""
import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


def main():
    parser = argparse.ArgumentParser(
        description="2D to 3D Converter using SAM 3D Objects",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Launch GUI application
  python main.py --gui

  # Convert with CLI (requires image and mask)
  python main.py --image input.jpg --mask mask.png --output output/

  # Visualize existing mesh
  python main.py --visualize output/mesh.obj
        """
    )

    parser.add_argument(
        "--gui",
        action="store_true",
        help="Launch Gradio GUI interface"
    )

    parser.add_argument(
        "--image",
        type=str,
        help="Path to input image"
    )

    parser.add_argument(
        "--mask",
        type=str,
        help="Path to segmentation mask"
    )

    parser.add_argument(
        "--output",
        type=str,
        default="data/output",
        help="Output directory (default: data/output)"
    )

    parser.add_argument(
        "--visualize",
        type=str,
        help="Path to mesh file to visualize"
    )

    parser.add_argument(
        "--depth",
        type=int,
        default=9,
        help="Poisson reconstruction depth (default: 9)"
    )

    parser.add_argument(
        "--format",
        type=str,
        default="obj",
        choices=["obj", "ply", "stl"],
        help="Output mesh format (default: obj)"
    )

    args = parser.parse_args()

    if args.gui:
        # Launch GUI
        from gui.app import App
        app = App()
        app.launch()

    elif args.visualize:
        # Visualize mesh
        from mesh_processing.mesh_converter import MeshConverter
        converter = MeshConverter()
        converter.visualize_mesh(args.visualize)

    elif args.image and args.mask:
        # CLI mode
        from sam_integration.sam_processor import SAMProcessor
        from mesh_processing.mesh_converter import MeshConverter
        from PIL import Image

        print("Running 2D to 3D conversion...")

        # Initialize processors
        sam_processor = SAMProcessor()
        mesh_converter = MeshConverter()

        # Load image and mask
        image = Image.open(args.image)
        mask = sam_processor.load_mask(args.mask)

        # Generate point cloud
        print("\nStep 1: Generating point cloud with SAM 3D Objects...")
        ply_path = sam_processor.generate_point_cloud(
            image,
            mask,
            output_dir=args.output
        )

        # Convert to watertight mesh
        print("\nStep 2: Converting to watertight mesh...")
        mesh_path = mesh_converter.convert_to_watertight_mesh(
            ply_path,
            output_dir=args.output,
            depth=args.depth,
            output_format=args.format
        )

        print(f"\n✓ Conversion complete!")
        print(f"  Point cloud: {ply_path}")
        print(f"  Watertight mesh: {mesh_path}")

    else:
        parser.print_help()
        print("\nError: Please specify --gui, --visualize, or provide --image and --mask")
        sys.exit(1)


if __name__ == "__main__":
    main()
