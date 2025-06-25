#!/bin/bash

echo
echo "🗑️ AIMD Uninstaller for Linux/macOS"
echo "=================================="
echo

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo "❌ ERROR: Root privileges required"
   echo
   echo "Please run this script with sudo:"
   echo "sudo ./uninstall-unix.sh"
   echo
   exit 1
fi

echo "⚠️  This will remove AIMD from your system"
echo
read -p "Are you sure you want to uninstall AIMD? (y/N): " confirm

if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "Uninstallation cancelled."
    exit 0
fi

echo
echo "🗑️ Removing AIMD files..."

# Remove global command
if [[ -f "/usr/local/bin/aimd" ]]; then
    rm "/usr/local/bin/aimd"
    echo "✅ Removed global aimd command"
else
    echo "⚠️  Global aimd command not found"
fi

# Remove AIMD directory
if [[ -d "/usr/local/lib/aimd" ]]; then
    rm -rf "/usr/local/lib/aimd"
    echo "✅ Removed AIMD directory"
else
    echo "⚠️  AIMD directory not found"
fi

echo
echo "✅ AIMD has been uninstalled successfully!"
echo
echo "💡 Note: Python dependencies were not removed"
echo "   If you want to remove them, run:"
echo "   pip3 uninstall certifi httpx requests pathspec tqdm"
echo
echo "🔑 Your GOOGLE_API_KEY environment variable was not removed"
echo "   If you want to remove it from your shell profile:"
echo "   Edit ~/.bashrc or ~/.zshrc and remove the export line"
echo