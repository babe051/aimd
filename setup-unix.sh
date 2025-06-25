#!/bin/bash

echo
echo "🚀 AIMD Setup for Linux/macOS"
echo "============================="
echo

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo "❌ ERROR: Root privileges required"
   echo
   echo "Please run this script with sudo:"
   echo "sudo ./setup-unix.sh"
   echo
   exit 1
fi

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: Python 3 is not installed"
    echo
    echo "Please install Python 3 first:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  macOS: brew install python3"
    echo "  CentOS/RHEL: sudo yum install python3 python3-pip"
    echo
    exit 1
fi

echo "✅ Python 3 is installed"
python3 --version

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ ERROR: pip3 is not installed"
    echo
    echo "Please install pip3 first:"
    echo "  Ubuntu/Debian: sudo apt install python3-pip"
    echo "  macOS: pip3 is included with Python"
    echo
    exit 1
fi

# Check if required files exist
if [[ ! -f "aimd.py" ]]; then
    echo "❌ ERROR: aimd.py not found in current directory"
    exit 1
fi

if [[ ! -f "generator.py" ]]; then
    echo "❌ ERROR: generator.py not found in current directory"
    exit 1
fi

if [[ ! -f "utils.py" ]]; then
    echo "❌ ERROR: utils.py not found in current directory"
    exit 1
fi

echo
echo "📦 Installing Python dependencies..."
pip3 install certifi httpx requests pathspec tqdm

if [[ $? -ne 0 ]]; then
    echo "❌ ERROR: Failed to install dependencies"
    exit 1
fi

# Create aimd directory
AIMD_DIR="/usr/local/lib/aimd"
echo
echo "📂 Creating AIMD directory: $AIMD_DIR"
mkdir -p "$AIMD_DIR"

# Copy files
echo "📂 Copying AIMD files..."
cp aimd.py "$AIMD_DIR/"
cp generator.py "$AIMD_DIR/"
cp utils.py "$AIMD_DIR/"

# Create the aimd command script
echo "📝 Creating global command..."
cat > /usr/local/bin/aimd << 'EOF'
#!/bin/bash
python3 /usr/local/lib/aimd/aimd.py "$@"
EOF

# Make it executable
chmod +x /usr/local/bin/aimd

echo
echo "✅ Installation completed successfully!"
echo
echo "🔑 IMPORTANT: Set your Google AI API key"
echo "   1. Get your API key from: https://aistudio.google.com/"
echo "   2. Add this line to your shell profile (~/.bashrc, ~/.zshrc, etc.):"
echo "      export GOOGLE_API_KEY='your-api-key-here'"
echo "   3. Reload your shell: source ~/.bashrc (or restart terminal)"
echo
echo "🚀 Usage examples:"
echo "   aimd /path/to/project"
echo "   aimd . -i node_modules '*.log'"
echo "   aimd . --output DOCS.md --max-files 100"
echo
echo "📁 Installation location: $AIMD_DIR"
echo "🔗 Command location: /usr/local/bin/aimd"
echo
echo "✨ You can now use 'aimd' from anywhere in your terminal!"