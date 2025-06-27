#!/bin/bash

echo ""
echo "🚀 AIMD Setup for Linux/macOS"
echo "============================="

# Require root permissions
if [ "$EUID" -ne 0 ]; then
    echo "❌ ERROR: Root privileges required"
    echo "Please run: sudo ./setup-unix.sh"
    exit 1
fi

# Detect project root (directory where this script lives)
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Check Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install it and try again."
    exit 1
fi

echo "✅ Python 3 is installed:"
python3 --version

# Create virtual environment
echo ""
echo "📦 Creating virtual environment at: $PROJECT_DIR/.venv"
python3 -m venv "$PROJECT_DIR/.venv"

if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment."
    exit 1
fi

# Activate venv and install requirements
echo ""
echo "📦 Installing dependencies..."
source "$PROJECT_DIR/.venv/bin/activate"
pip install --upgrade pip
pip install -r "$PROJECT_DIR/requirements.txt"

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies."
    deactivate
    exit 1
fi
deactivate

# Create global launcher
echo ""
echo "⚙️ Installing 'aimd' command..."

LAUNCHER_PATH="/usr/local/bin/aimd"
cat <<EOF > "$LAUNCHER_PATH"
#!/bin/bash
source "$PROJECT_DIR/.venv/bin/activate"
python "$PROJECT_DIR/aimd.py" "\$@"
EOF

chmod +x "$LAUNCHER_PATH"

# Done
echo ""
echo "✅ AIMD installed globally!"
echo "👉 You can now run it from anywhere like:"
echo ""
echo "   aimd /path/to/your/project --output README.md"
echo "   aimd . --ar                    # Generate in Arabic"
echo "   aimd . --fr                    # Generate in French"
echo "   aimd . -i node_modules *.log   # With custom ignores"
echo ""