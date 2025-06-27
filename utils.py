import os
import threading
import time
import certifi
from httpx import Client
import requests
import pathspec
from tqdm import tqdm

# Set up a secure HTTP client
http_client = Client(verify=certifi.where())

def analyze_path(path, ignore_files=None, ignore_dirs=None, custom_ignores=None):
    ignore_files = ignore_files or []
    ignore_dirs = ignore_dirs or []
    custom_ignores = custom_ignores or []

    # Always ignore these common directories and files
    default_ignores = [
        '.git/', 'node_modules/', '__pycache__/', '.DS_Store', '*.pyc', '*.pyo', 
        '*.pyd', '*.log', '.env', 'dist/', 'build/', '.venv/', '*.egg-info/',
        '.coverage', 'htmlcov/', '.pytest_cache/', '.mypy_cache/', '.tox/',
        '.idea/', '.vscode/', '*.sqlite3', '*.db', 'coverage/', '.firebase/',
        'functions/node_modules/', 'functions/lib/', '*.map', '*.min.js'
    ]

    gitignore_path = os.path.join(path, ".gitignore")
    gitignore_lines = default_ignores.copy()
    
    # Add custom ignores from command line
    if custom_ignores:
        print(f"🚫 Adding custom ignores: {', '.join(custom_ignores)}")
        gitignore_lines.extend(custom_ignores)
    
    if os.path.isfile(gitignore_path):
        with open(gitignore_path, "r", encoding="utf-8", errors="ignore") as f:
            gitignore_content = f.read()
            # Clean up the gitignore content - remove empty lines and comments
            for line in gitignore_content.splitlines():
                line = line.strip()
                if line and not line.startswith('#'):
                    gitignore_lines.append(line)
    
    pspec = pathspec.PathSpec.from_lines("gitwildmatch", gitignore_lines)

    def is_ignored(full_path):
        # Get relative path from the root directory
        try:
            rel_path = os.path.relpath(full_path, start=path).replace("\\", "/")
        except ValueError:
            # Handle case where paths are on different drives (Windows)
            return False
        
        # Quick checks for common ignores
        filename = os.path.basename(rel_path)
        if filename.startswith('.') and filename in ['.DS_Store', '.env', '.coverage']:
            return True
        
        # Check if any part of the path contains ignored directories
        path_parts = rel_path.split("/")
        for part in path_parts:
            if part in ['.git', 'node_modules', '__pycache__', '.venv', '.pytest_cache', '.mypy_cache', '.idea', '.vscode', 'dist', 'build', '.firebase']:
                return True
        
        # Check custom ignores from command line
        if custom_ignores:
            for ignore_pattern in custom_ignores:
                # Handle directory patterns (with or without trailing slash)
                if ignore_pattern.endswith('/'):
                    ignore_dir = ignore_pattern.rstrip('/')
                    if ignore_dir in path_parts:
                        return True
                # Handle file patterns
                elif ignore_pattern in filename or ignore_pattern == filename:
                    return True
                # Handle wildcard patterns
                elif '*' in ignore_pattern:
                    import fnmatch
                    if fnmatch.fnmatch(filename, ignore_pattern):
                        return True
                # Handle exact path matches
                elif ignore_pattern in rel_path or rel_path.endswith(ignore_pattern):
                    return True
        
        # Check gitignore patterns
        if pspec:
            # Check if the file/directory itself matches
            if pspec.match_file(rel_path):
                return True
            # For directories, also check if directory path with trailing slash matches
            if os.path.isdir(full_path):
                if pspec.match_file(rel_path + "/"):
                    return True
        
        # Check additional ignore directories
        for ignore_dir in ignore_dirs:
            if ignore_dir in path_parts:
                return True
        
        # Check additional ignore files
        for ignore_file in ignore_files:
            if filename == ignore_file:
                return True
        
        return False

    result = ""
    file_paths = []

    # Walk through directory structure
    for root, dirs, files in os.walk(path, topdown=True):
        # Filter out ignored directories in-place to prevent walking into them
        dirs_to_remove = []
        for d in dirs:
            dir_path = os.path.join(root, d)
            if is_ignored(dir_path):
                dirs_to_remove.append(d)
        
        for d in dirs_to_remove:
            dirs.remove(d)
        
        # Add non-ignored files to the list
        for file in files:
            file_path = os.path.join(root, file)
            if not is_ignored(file_path):
                file_paths.append(file_path)

    # Process all files (no limit)
    total_files = len(file_paths)

    # Read and process files with progress bar
    with tqdm(total=total_files, desc="📂 Processing files", 
              bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]") as pbar:
        for i, file_path in enumerate(file_paths):
            rel_path = os.path.relpath(file_path, start=path).replace("\\", "/")
            
            # Update progress bar description with current file
            pbar.set_description(f"📂 Reading: {rel_path[:40]}{'...' if len(rel_path) > 40 else ''}")
            
            result += f"\n--- {rel_path} ---\n"
            try:
                # Skip binary files and very large files
                file_size = os.path.getsize(file_path)
                if file_size > 5000000:  # Skip files larger than 5MB
                    result += f"(File too large - {file_size} bytes, skipped)\n"
                    pbar.update(1)
                    continue
                    
                # Check if file is likely binary
                try:
                    with open(file_path, "rb") as f:
                        sample = f.read(1024)
                        if b'\0' in sample:  # Null bytes indicate binary file
                            result += "(Binary file, skipped)\n"
                            pbar.update(1)
                            continue
                except:
                    pass
                
                # Try to read as text file
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    # Limit file content size to prevent huge prompts
                    if len(content) > 5000:
                        content = content[:5000] + "\n... (file truncated due to size)"
                    result += content + "\n"
            except Exception as e:
                result += f"(Could not read {rel_path}: {e})\n"
            
            pbar.update(1)

    return result if result else "No readable files found."

def ask_openai(prompt, lang="en"):
    api_key = "AIzaSyDM73o7B6NFDfhDqS8ZGrzOrnrErvTGveE"
    if not api_key:
        raise Exception("GOOGLE_API_KEY not found in environment variables.")

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    body = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    # Fun animation while waiting for API response with language info
    import sys
    animation_running = True
    
    lang_names = {"en": "English", "ar": "Arabic", "fr": "French"}
    current_lang = lang_names.get(lang, "English")
    
    def animate():
        frames = [
            f"🧠 Generating README in {current_lang}   ",
            f"🤖 Generating README in {current_lang}   ",
            f"⚡ Generating README in {current_lang}   ",
            f"✨ Generating README in {current_lang}   ",
            f"🔥 Generating README in {current_lang}   ",
            f"💭 Generating README in {current_lang}   "
        ]
        idx = 0
        while animation_running:
            print(f"\r{frames[idx % len(frames)]}", end="", flush=True)
            time.sleep(0.3)
            idx += 1
    
    animation_thread = threading.Thread(target=animate)
    animation_thread.daemon = True
    animation_thread.start()
    
    try:
        response = requests.post(f"{url}?key={api_key}", headers=headers, json=body)
        response.raise_for_status()
        data = response.json()
        
        # Stop animation
        animation_running = False
        animation_thread.join(timeout=0.1)
        
        if "candidates" in data and len(data["candidates"]) > 0:
            print(f"\r🎉 README generated successfully in {current_lang}!           ")
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        else:
            print("\r❌ No valid response received                ")
            return "Error: No valid response received from Google AI"
                
    except requests.exceptions.RequestException as e:
        animation_running = False
        animation_thread.join(timeout=0.1)
        print(f"\r❌ Connection failed: {e}                    ")
        return "Error: Failed to connect to Google AI Studio"
    except KeyError as e:
        animation_running = False
        animation_thread.join(timeout=0.1)
        print(f"\r❌ Response error: Invalid format            ")
        print("🔍 Full response:", response.text if 'response' in locals() else "No response")
        return "Error: Invalid response format from Google AI Studio"
    except Exception as e:
        animation_running = False
        animation_thread.join(timeout=0.1)
        print(f"\r❌ Unexpected error occurred                 ")
        return "Error: An unexpected error occurred"