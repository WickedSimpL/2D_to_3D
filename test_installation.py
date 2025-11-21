#!/usr/bin/env python3
"""
Test script to verify that all dependencies are properly installed
"""
import sys
from importlib import import_module


def test_import(module_name, package_name=None):
    """Test if a module can be imported"""
    display_name = package_name or module_name
    try:
        mod = import_module(module_name)
        version = getattr(mod, '__version__', 'unknown version')
        print(f"✓ {display_name:25s} - {version}")
        return True
    except ImportError as e:
        print(f"✗ {display_name:25s} - NOT INSTALLED")
        print(f"  Error: {e}")
        return False


def check_cuda():
    """Check CUDA availability"""
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✓ CUDA available          - {torch.cuda.get_device_name(0)}")
            print(f"  CUDA version: {torch.version.cuda}")
            return True
        else:
            print("⚠ CUDA not available      - Will use CPU (slower)")
            return False
    except Exception as e:
        print(f"✗ Error checking CUDA: {e}")
        return False


def check_directories():
    """Check if required directories exist"""
    import os
    dirs = ['data/input', 'data/output', 'examples', 'src/gui', 'src/sam_integration', 'src/mesh_processing']

    all_exist = True
    for dir_path in dirs:
        if os.path.exists(dir_path):
            print(f"✓ Directory exists: {dir_path}")
        else:
            print(f"✗ Directory missing: {dir_path}")
            all_exist = False

    return all_exist


def check_sam_3d_objects():
    """Check if SAM 3D Objects is installed"""
    try:
        from sam_3d_objects.inference import Inference
        print("✓ SAM 3D Objects          - Installed")
        return True
    except ImportError:
        print("✗ SAM 3D Objects          - NOT INSTALLED")
        print("  Install from: https://github.com/facebookresearch/sam-3d-objects")
        return False


def main():
    print("=" * 70)
    print("2D to 3D Converter - Installation Test")
    print("=" * 70)

    print("\n[1/4] Checking Core Dependencies...")
    print("-" * 70)

    core_modules = [
        ("numpy", "NumPy"),
        ("PIL", "Pillow"),
        ("torch", "PyTorch"),
        ("torchvision", "TorchVision"),
    ]

    core_ok = all(test_import(mod, name) for mod, name in core_modules)

    print("\n[2/4] Checking GUI Dependencies...")
    print("-" * 70)

    gui_modules = [
        ("gradio", "Gradio"),
        ("cv2", "OpenCV"),
    ]

    gui_ok = all(test_import(mod, name) for mod, name in gui_modules)

    print("\n[3/4] Checking 3D Processing Dependencies...")
    print("-" * 70)

    mesh_modules = [
        ("open3d", "Open3D"),
        ("trimesh", "Trimesh"),
        ("scipy", "SciPy"),
        ("sklearn", "scikit-learn"),
    ]

    mesh_ok = all(test_import(mod, name) for mod, name in mesh_modules)

    print("\n[4/4] Checking SAM 3D Objects...")
    print("-" * 70)
    sam_ok = check_sam_3d_objects()

    print("\n[5/5] Checking CUDA...")
    print("-" * 70)
    cuda_ok = check_cuda()

    print("\n[6/6] Checking Project Structure...")
    print("-" * 70)
    dirs_ok = check_directories()

    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)

    results = {
        "Core Dependencies": core_ok,
        "GUI Dependencies": gui_ok,
        "3D Processing": mesh_ok,
        "SAM 3D Objects": sam_ok,
        "CUDA Support": cuda_ok,
        "Project Structure": dirs_ok,
    }

    for component, status in results.items():
        status_icon = "✓" if status else "✗"
        print(f"{status_icon} {component}")

    all_ok = all(results.values())

    if all_ok:
        print("\n🎉 All checks passed! Your installation is ready.")
        print("\nNext steps:")
        print("  1. Download SAM 3D Objects checkpoints")
        print("  2. Run: python main.py --gui")
        return 0
    else:
        print("\n⚠ Some components are missing or not working properly.")
        print("\nPlease check:")
        print("  - Run: pip install -r requirements.txt")
        print("  - Install SAM 3D Objects: https://github.com/facebookresearch/sam-3d-objects")
        print("  - See SETUP.md for detailed instructions")
        return 1


if __name__ == "__main__":
    sys.exit(main())
