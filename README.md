# AIMD - AI Markdown Generator

**AIMD** is a powerful command-line tool that automatically generates professional README.md files for your projects using Google's Gemini AI. Simply point it at any project directory and watch it create comprehensive documentation in seconds!

## 🚀 Quick Installation

### Prerequisites

- Python 3.6 or higher
- Google AI Studio API key ([Get yours here](https://aistudio.google.com/app/apikey))
- Internet connection

### Windows
```cmd
git clone https://github.com/babe051/aimd.git
cd aimd
# Run as Administrator
setup-windows.bat
```

### Linux/macOS
```bash
git clone https://github.com/babe051/aimd.git
cd aimd
chmod +x setup-unix.sh
sudo ./setup-unix.sh
```

## 📖 Usage

After installation, use `aimd` from any directory:

```bash
# Generate a README for the current directory
aimd .

# Generate a README for a specific project
aimd /path/to/project

# Windows example
aimd C:\Users\username\projects\myapp

# Ignore specific files/directories
aimd . -i node_modules "*.log" temp/

# Custom output filename and file limit
aimd . --output DOCUMENTATION.md --max-files 100

# Multiple ignore patterns
aimd . -i "*.pyc" "__pycache__/" ".env*" "logs/"

# Generate documentation in Arabic
aimd . --ar

# Generate documentation in French
aimd . --fr
```

## 🛠️ Command Options


| Option         | Description                                 | Example                   |
|----------------|---------------------------------------------|---------------------------|
| `path`         | Project directory to analyze                | `aimd /projects/webapp`   |
| `--output`     | Output filename (default: README.md)        | `--output DOCS.md`        |
| `--max-files`  | Maximum files to process (default: 50)      | `--max-files 100`         |
| `-i, --ignore` | Additional files/dirs to ignore             | `-i logs/ "*.tmp"`        |
| `--ar`         | Generate documentation in Arabic            | `--ar`                    |
| `--fr`         | Generate documentation in French            | `--fr`                    |

---

## ⚙️ Features

- 🤖 **AI-Powered**: Uses Google Gemini AI for intelligent documentation
- 📂 **Smart Analysis**: Automatically detects project structure and tech stack
- 🚫 **Intelligent Filtering**: Respects `.gitignore` and custom ignore patterns
- 🎯 **Cross-Platform**: Works on Windows, Linux, and macOS
- ⚡ **Fast Processing**: Progress bars and efficient file handling
- 🎨 **Professional Output**: GitHub-ready markdown with emojis and structure

## 📁 What Gets Analyzed

AIMD intelligently processes your project:

✅ **Includes:**
- Source code files (`.py`, `.js`, `.html`, `.css`, etc.)
- Configuration files (`package.json`, `requirements.txt`, etc.)
- Documentation files
- Project structure and dependencies

❌ **Automatically Ignores:**
- `.git/` directory
- `node_modules/` directory
- `__pycache__/` directory
- Binary files and images
- Large files (>5MB)
- Files matching `.gitignore` patterns

## 📊 Example Output

```bash
$ aimd .
🚀 Starting AIMD - AI Markdown Generator
📂 Target path: /home/user/myproject
📄 Output file: /home/user/myproject/README.md (in target directory)
--------------------------------------------------
🔍 Analyzing: /home/user/myproject...
📄 README will be saved to: /home/user/myproject/README.md
📂 Processing files |████████████| 25/50 [00:02<00:01]
🎉 README generated successfully!
✅ README.md generated successfully at /home/user/myproject/README.md
--------------------------------------------------
🎉 All done! Your README.md has been generated successfully.
📁 Location: /home/user/myproject/README.md
```

## 🗂️ Installation File Structure

### Windows
```
C:\Windows\System32\aimd\
├── aimd.py          # Main script
├── generator.py     # Generation logic
├── utils.py         # Utilities
└── aimd.bat         # Local command script

C:\Windows\System32\
└── aimd.bat         # Global command (calls local script)
```

### Linux/macOS
```
/usr/local/lib/aimd/
├── aimd.py          # Main script
├── generator.py     # Generation logic
└── utils.py         # Utilities

/usr/local/bin/
└── aimd             # Global command script
```

## 🗑️ Uninstallation

### Windows
```cmd
# Run as Administrator
uninstall-windows.bat
```

### Linux/macOS
```bash
sudo ./uninstall-unix.sh
```

### Manual Uninstall
**Windows:**
```cmd
del "C:\Windows\System32\aimd.bat"
rmdir /s "C:\Windows\System32\aimd"
```

**Linux/macOS:**
```bash
sudo rm /usr/local/bin/aimd
sudo rm -rf /usr/local/lib/aimd
```

## 🔧 Troubleshooting

### Common Issues


**"Permission denied" during installation**
- **Windows**: Run setup as Administrator
- **Linux/Mac**: Use `sudo ./setup-unix.sh`

**"Command not found: aimd"**
- Verify the setup script completed successfully
- Try opening a new terminal window
- Check if the files exist in the installation directories

**"No readable files found"**
- Ensure the target directory contains source code
- Check if your ignore patterns are too restrictive
- Try increasing `--max-files` limit

**"Failed to connect to Google AI Studio"**
- Check your internet connection
- Verify your API key is valid and active
- Ensure the API key has proper permissions

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🛡️ Security

- **API Key Safety**: Never hardcode API keys in source code
- **Environment Variables**: Always use environment variables for sensitive data
- **File Permissions**: Setup scripts properly handle file permissions
- **Safe Installation**: Files are placed in standard system directories

## 🔄 Version History

- **v1.0.0**: Initial release with cross-platform support
- Full AI-powered README generation
- Smart file filtering and gitignore support
- Progress bars and animated feedback
- Global command installation

---
## 👥 Contributors

- [<img src="https://github.com/babe051.png" width="32" height="32" style="border-radius:50%"/>](https://github.com/babe051)  
  **Mohamed Val** – [@babe051](https://github.com/babe051)

- [<img src="https://github.com/Zeini-23025.png" width="32" height="32" style="border-radius:50%"/>](https://github.com/Zeini-23025)  
  **Zeini Cheikh** – [@Zeini-23025](https://github.com/Zeini-23025)

**Made with ❤️ for developers who love good documentation! 🚀📝**