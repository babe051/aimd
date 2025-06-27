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

    # Limit to specified maximum files for better performance
    total_files = len(file_paths)

    # Read and process files with progress bar
    with tqdm(total=total_files, desc="📂 Processing files", 
              bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]") as pbar:
        for i, file_path in enumerate(file_paths[:total_files]):
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
    

def generate_readme_from_path(path, output_file, custom_ignores=None, lang="en"):
    # Validate input path
    if not os.path.exists(path):
        print(f"❌ Error: Path '{path}' does not exist.")
        return False
    
    # If output_file is just a filename (like "README.md"), save it in the target directory
    if not os.path.dirname(output_file):
        output_file = os.path.join(path, output_file)
    
    print(f"🔍 Analyzing: {path}...")
    print(f"📄 README will be saved to: {output_file}")
    
    try:
        summary = analyze_path(path, custom_ignores=custom_ignores)
        
        if summary == "No readable files found.":
            print("⚠️  Warning: No readable files found in the specified path.")
            return False
        
        # Base prompt in English
        base_prompt = f"""
You are a professional technical writer and README expert.

Your task is to generate a **high-quality `README.md` file** for a software project based on the following summarized file structure and content:

{summary}

---

🎯 **Objective**  
Your README must be:
- Clear, concise, and professional
- Written in **Markdown**, using emojis, icons, tables, and code blocks to improve readability
- Friendly to both developers and users
- GitHub-ready and suitable for both public repositories and internal teams

---

🧠 **Core Guidelines**  
1. **Do not invent** information not seen in the provided structure or code.
2. If a section is relevant but cannot be filled from the files, write:  
   _"This section should be filled in by the project maintainer."_
3. If no UI is found, skip screenshots or page descriptions.

---

📊 **Adapt Based on Project Type**  
If the project appears to be:
- 🔧 **Backend-only**: Focus more on API documentation, setup, and environment configuration
- 🎨 **Frontend-only**: Emphasize pages, components, and how the UI works
- 🧩 **Full-stack**: Follow the default order, combining both frontend and backend documentation

Reorder and prioritize sections accordingly.

---

📚 **Sections to Include (Only If Applicable)**

---

### 🧠 Overview  
- What this project does  
- Who it is for  
- What problem it solves  
- Include a short tagline (optional)

---

### ⚙️ Features  
- Bullet-point or checkmark list of key functionalities  
- Separate frontend and backend features when relevant

---

### 📂 Project Structure  
Describe what each key file or folder does (especially: `/routes`, `/src`, `/components`, `/api`, `/services`, `/tests`, etc.)

---

### 🌐 API Endpoints (if detected)  
Document available endpoints using a Markdown table:

| Method | Endpoint        | Description         | Input Params         | Response             |
|--------|------------------|---------------------|-----------------------|-----------------------|
| POST   | `/api/login`     | User authentication | `email`, `password`  | `200 OK` + JWT token  |
| GET    | `/api/users`     | List all users      | None                 | JSON array of users   |

If no API is present, skip this section.

---

### 🖼️ Frontend Pages  
- List screens/views and their purposes  
- Mention any component reuse or interactions  
- If UI exists, suggest screenshot placeholders using Markdown:

```markdown
![Login Page](screenshots/login.png)
```

### 🛠 Tech Stack
List core technologies used, such as:

- Programming languages (Python, JavaScript, etc.)
- Frameworks (React, Angular, Flask, Spring Boot, etc.)
- Libraries or services (Firebase, Stripe, MongoDB, etc.)

Example:
🧰 React • Node.js • Express • MongoDB • Tailwind CSS • Docker

### 🚀 Getting Started
Provide clear installation and run instructions:

```bash
# Clone the repository
git clone https://github.com/user/project.git

# Install dependencies
npm install

# Run the application
npm start
```

Also mention:
- Environment variable setup
- URLs or ports (http://localhost:3000)

### 🔐 Environment Variables
If .env or config files exist, include a table:

| Variable       | Description           | Example           |
| -------------- | --------------------- | ----------------- |
| `DATABASE_URL` | PostgreSQL connection | `postgres://...`  |
| `JWT_SECRET`   | Token signing key     | `your-secret-key` |

### 🧪 Testing
If tests exist, explain:
- How to run them (e.g. npm test, pytest)
- Testing framework (Jest, Mocha, etc.)
- Where test files are located

### 🚀 Deployment
Document:
- Build steps (npm run build, etc.)
- Hosting provider (Heroku, Vercel, etc.)
- CI/CD instructions (if files like .github/workflows/ or Dockerfile exist)

### 🔐 Authentication & Security
If authentication is implemented:
- Specify login methods (OAuth, JWT, session-based)
- Mention protected routes
- Roles (if any)

### 📬 Author / Contact
If authorship data is present:
- Include name, email, GitHub, LinkedIn, etc.

### 🔖 License
If a license file exists (e.g. LICENSE, MIT, GPL), include the correct license name and a short sentence like:

This project is licensed under the MIT License.

### 📌 Formatting Rules

- Use ### for section headings
- Use emoji icons to make sections visually scannable
- Prefer Markdown tables and bullet points for clarity
- Use fenced code blocks (```bash or ```json) for command-line or config examples
"""

        # Add language-specific instructions
        if lang == "fr":
            prompt = base_prompt + """

IMPORTANT: Generate the entire README in French (Français). 
- Use proper French technical terminology
- Maintain the same structure and formatting
- Keep code examples and technical elements in their original form (URLs, commands, etc.)
- Translate all descriptive text, headings, and documentation to French
"""
        elif lang == "ar":
            prompt = base_prompt + """

IMPORTANT: Generate the entire README in Arabic (العربية). 
- Use proper Arabic technical terminology
- Maintain the same structure and formatting
- Keep code examples and technical elements in their original form (URLs, commands, etc.)
- Translate all descriptive text, headings, and documentation to Arabic
- Use right-to-left text direction where appropriate
- Keep emojis and Markdown formatting
"""
        else:
            prompt = base_prompt

        markdown = ask_openai(prompt, lang)
        
        if markdown.startswith("Error:"):
            print(f"❌ {markdown}")
            return False

        # Check if README already exists
        if os.path.exists(output_file):
            print(f"⚠️  README.md already exists at: {output_file}")
            print("🔄 It will be replaced with the new generated version.")
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Write the README file with proper UTF-8 encoding for all languages
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(markdown)
        
        print(f"✅ README.md generated successfully at {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error during README generation: {e}")
        return False