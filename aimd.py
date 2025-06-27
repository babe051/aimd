#!/usr/bin/env python3
# aimd.py
import argparse
import sys
import os
from generator import generate_readme_from_path

def main():
    parser = argparse.ArgumentParser(
        description="AIMD - AI Markdown Generator",
        epilog="Example: aimd /path/to/project --output my-readme.md -i node_modules .env --ar"
    )
    parser.add_argument("path", help="Path to file or directory to analyze")
    parser.add_argument("--output", default="README.md", 
                       help="Output README filename (default: README.md)")
    parser.add_argument("--max-files", type=int, default=50,
                       help="Maximum number of files to process (default: 50)")
    parser.add_argument("-i", "--ignore", nargs="*", default=[],
                       help="Additional files or directories to ignore (e.g., -i temp.txt logs/ config.json)")
    
    # Language options
    lang_group = parser.add_mutually_exclusive_group()
    lang_group.add_argument("--ar", action="store_true",
                           help="Generate README in Arabic")
    lang_group.add_argument("--fr", action="store_true",
                           help="Generate README in French")
    
    args = parser.parse_args()
    
    # Validate input path
    if not os.path.exists(args.path):
        print(f"❌ Error: The path '{args.path}' does not exist.")
        sys.exit(1)
    
    # Determine language
    language = "en"  # Default to English
    if args.ar:
        language = "ar"
    elif args.fr:
        language = "fr"
    
    print(f"🚀 Starting AIMD - AI Markdown Generator")
    print(f"📂 Target path: {args.path}")
    
    # Determine the actual output path
    if not os.path.dirname(args.output):
        actual_output = os.path.join(args.path, args.output)
        print(f"📄 Output file: {actual_output} (in target directory)")
    else:
        actual_output = args.output
        print(f"📄 Output file: {actual_output}")
    
    # Show language selection
    lang_names = {"en": "English", "ar": "Arabic (العربية)", "fr": "French (Français)"}
    print(f"🌐 Language: {lang_names[language]}")
    
    print(f"")
    
    # Show ignored items if any
    if args.ignore:
        print(f"🚫 Additional ignores: {', '.join(args.ignore)}")
    
    print("-" * 50)
    
    success = generate_readme_from_path(args.path, args.output, args.ignore, language)
    
    if success:
        print("-" * 50)
        print("🎉 All done! Your README.md has been generated successfully.")
        if not os.path.dirname(args.output):
            print(f"📁 Location: {os.path.join(args.path, args.output)}")
        sys.exit(0)
    else:
        print("-" * 50)
        print("❌ README generation failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()