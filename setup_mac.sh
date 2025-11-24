#!/bin/bash
# Quick setup script for macOS
# This script automates the installation process for Mac users

set -e  # Exit on error

echo "=================================================="
echo "2D to 3D Converter - Mac Setup Script"
echo "=================================================="
echo ""

# Detect Mac architecture
ARCH=$(uname -m)
if [[ "$ARCH" == "arm64" ]]; then
    echo "✓ Detected: Apple Silicon Mac (M1/M2/M3)"
    IS_APPLE_SILICON=true
else
    echo "✓ Detected: Intel Mac"
    IS_APPLE_SILICON=false
fi

# Check Python version
echo ""
echo "[1/6] Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo "✓ Python $PYTHON_VERSION found"
else
    echo "✗ Python 3 not found"
    echo ""
    echo "Please install Python 3.8+ using Homebrew:"
    echo "  brew install python@3.11"
    exit 1
fi

# Create virtual environment
echo ""
echo "[2/6] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠ Virtual environment already exists, skipping..."
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "[3/6] Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Install PyTorch
echo ""
echo "[4/6] Installing PyTorch..."
if $IS_APPLE_SILICON; then
    echo "Installing PyTorch with MPS (Metal) support for Apple Silicon..."
    pip install --upgrade pip
    pip install torch torchvision torchaudio
else
    echo "Installing PyTorch (CPU) for Intel Mac..."
    pip install --upgrade pip
    pip install torch torchvision torchaudio
fi
echo "✓ PyTorch installed"

# Install requirements
echo ""
echo "[5/6] Installing project dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Verify installation
echo ""
echo "[6/6] Verifying installation..."
python test_installation.py

echo ""
echo "=================================================="
echo "Installation Complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Install SAM 3D Objects:"
echo "   cd .."
echo "   git clone https://github.com/facebookresearch/sam-3d-objects.git"
echo "   cd sam-3d-objects"
echo "   pip install -e ."
echo "   cd ../2D_to_3D"
echo ""
echo "2. Download model checkpoints"
echo "   See: https://github.com/facebookresearch/sam-3d-objects"
echo ""
echo "3. Run the application:"
echo "   source venv/bin/activate"
echo "   python main.py --gui"
echo ""
echo "For detailed instructions, see SETUP_MAC.md"
echo ""
