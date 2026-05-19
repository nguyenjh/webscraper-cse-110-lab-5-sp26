#!/usr/bin/env python3
import sys
import requests
import re
from urllib.parse import urlparse

def parse_repo_url(url):
    """Extract owner and repo name from GitHub URL."""
    if "github.com" in url:
        parts = url.rstrip('/').split('/')
        owner = parts[-2]
        repo = parts[-1]
    else:
        owner, repo = url.split('/')[-2:]
    return owner, repo

def check_file_exists_raw(owner, repo, filepath, branch="main"):
    """
    Check if a file exists in the repository using raw.githubusercontent.com.
    This actually fetches the file content to verify existence.
    """
    # Try main branch first, then master
    for try_branch in [branch, "main", "master"]:
        raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{try_branch}/{filepath}"
        try:
            response = requests.get(raw_url, timeout=10)
            if response.status_code == 200:
                return True, try_branch
        except requests.exceptions.RequestException:
            continue
    return False, None

def get_file_content(owner, repo, filepath):
    """Fetch the actual content of a file from the repository."""
    for branch in ["main", "master"]:
        raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{filepath}"
        try:
            response = requests.get(raw_url, timeout=10)
            if response.status_code == 200:
                return response.text
        except:
            continue
    return None

def get_repo_tree(owner, repo):
    """Use GitHub API to get the repository file tree structure."""
    api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            files = [item['path'] for item in data.get('tree', []) if item['type'] == 'blob']
            return files
    except:
        pass
    
    # Fallback: try master branch
    api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/master?recursive=1"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            files = [item['path'] for item in data.get('tree', []) if item['type'] == 'blob']
            return files
    except:
        pass
    
    return []

def scrape_student_repo(repo_url):
    """Scrape and validate a student's repository."""
    print("=" * 70)
    print(f"🔍 SCRAPING: {repo_url}")
    print("=" * 70)
    
    # Parse repository
    owner, repo = parse_repo_url(repo_url)
    print(f"\n📂 Repository: {owner}/{repo}")
    
    # Method 1: Get complete file tree via GitHub API (most reliable)
    print("\n📁 Scanning repository structure...")
    file_tree = get_repo_tree(owner, repo)
    
    if file_tree:
        print(f"   Found {len(file_tree)} files in repository")
        
        # Check for required files in the file tree
        required_files = {
            "expose.html": "expose.html",
            "explore.html": "explore.html",
            "README.md": "README.md",
            "expose.js": "assets/scripts/expose.js",
            "explore.js": "assets/scripts/explore.js",  # Optional but good
            "package.json": "package.json",
            "unit.test.js": "__tests__/unit.test.js"
        }
        
        print("\n📋 Required Files Check:")
        found_files = {}
        for name, path in required_files.items():
            # Check exact path match
            if path in file_tree:
                found_files[name] = True
                print(f"   ✅ {name} ({path})")
            else:
                # Try partial match for JavaScript files
                if path.endswith('.js'):
                    matching = [f for f in file_tree if f.endswith(path.split('/')[-1])]
                    if matching:
                        found_files[name] = True
                        print(f"   ✅ {name} (found as: {matching[0]})")
                    else:
                        found_files[name] = False
                        print(f"   ❌ {name} ({path}) - NOT FOUND")
                else:
                    found_files[name] = False
                    print(f"   ❌ {name} ({path}) - NOT FOUND")
    else:
        print("   ⚠️  Could not get file tree via API, trying direct file access...")
        
        # Method 2: Direct file checking (fallback)
        files_to_check = [
            ("expose.html", "expose.html"),
            ("explore.html", "explore.html"),
            ("README.md", "README.md"),
            ("expose.js", "assets/scripts/expose.js"),
            ("package.json", "package.json"),
        ]
        
        print("\n📋 Required Files Check:")
        found_files = {}
        for name, path in files_to_check:
            exists, branch = check_file_exists_raw(owner, repo, path)
            found_files[name] = exists
            print(f"   {'✅' if exists else '❌'} {name} ({path})")
            if exists:
                print(f"       → Found in branch: {branch}")
    
    # Get README content for student names
    print("\n👥 Extracting Student Information:")
    readme_content = get_file_content(owner, repo, "README.md")
    if readme_content:
        print("   ✅ README.md content retrieved")
        
        # Extract student names
        lines = readme_content.split('\n')[:25]
        names_found = []
        
        for line in lines:
            line = line.strip()
            # Look for "Name: Scott Pham" pattern
            name_match = re.search(r'^\*?name\*?\s*:\s*(.+)$', line, re.IGNORECASE)
            if name_match:
                names_found.append(name_match.group(1).strip())
            # Look for standalone name at beginning of README
            elif re.match(r'^[A-Z][a-z]+ [A-Z][a-z]+$', line) and len(line) < 40:
                if line not in ["Lab", "About", "Resources", "Activity"]:
                    names_found.append(line)
        
        if names_found:
            print(f"   👤 Student(s): {', '.join(names_found)}")
        else:
            print("   ⚠️  Could not extract names automatically")
            print(f"   First few lines of README:\n   {chr(10).join(['   ' + l for l in lines[:5] if l])}")
    else:
        print("   ❌ Could not retrieve README.md")
    
    # Check GitHub Pages
    print("\n🌐 GitHub Pages Deployment:")
    pages_url = f"https://{owner}.github.io/{repo}"
    expose_pages = f"{pages_url}/expose.html"
    explore_pages = f"{pages_url}/explore.html"
    
    try:
        expose_response = requests.get(expose_pages, timeout=10)
        if expose_response.status_code == 200:
            print(f"   ✅ expose.html deployed at: {expose_pages}")
        else:
            print(f"   ❌ expose.html NOT accessible at: {expose_pages}")
        
        explore_response = requests.get(explore_pages, timeout=10)
        if explore_response.status_code == 200:
            print(f"   ✅ explore.html deployed at: {explore_pages}")
        else:
            print(f"   ❌ explore.html NOT accessible at: {explore_pages}")
            
    except requests.exceptions.RequestException:
        print(f"   ❌ Could not reach GitHub Pages at: {pages_url}")
    
    # Check for GitHub Actions
    print("\n⚙️  GitHub Actions:")
    actions_path = ".github/workflows/main.yml"
    has_actions, _ = check_file_exists_raw(owner, repo, actions_path)
    print(f"   {'✅' if has_actions else '❌'} {'Found' if has_actions else 'Not found'}: {actions_path}")
    
    # Check for screenshot files
    print("\n📸 Required Screenshots:")
    screenshots = {
        "myError.png": "Error screenshot",
        "merged.png": "Merge screenshot"
    }
    
    for screenshot, description in screenshots.items():
        exists, _ = check_file_exists_raw(owner, repo, screenshot)
        print(f"   {'✅' if exists else '❌'} {screenshot} ({description})")
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 SCRAPING SUMMARY")
    print("=" * 70)
    
    # Calculate score
    total_items = len([k for k in found_files.keys() if k not in ["explore.js"]])  # explore.js is optional
    passed_items = sum(1 for k, v in found_files.items() if v and k not in ["explore.js"])
    
    # Add GitHub Pages to score
    pages_working = False
    if expose_response.status_code == 200:
        passed_items += 1
        pages_working = True
    total_items += 1
    
    # Add Actions to score
    if has_actions:
        passed_items += 1
    total_items += 1
    
    # Add screenshots to score
    for screenshot in screenshots:
        if screenshot in [s for s, _ in screenshots.items()]:
            exists, _ = check_file_exists_raw(owner, repo, screenshot)
            if exists:
                passed_items += 1
            total_items += 1
    
    score_percentage = (passed_items / total_items) * 100 if total_items > 0 else 0
    
    print(f"\n✅ Files found: {passed_items}/{total_items}")
    print(f"📈 Score: {score_percentage:.1f}%")
    
    # Provide specific feedback
    print("\n💡 FEEDBACK:")
    if not found_files.get("expose.html", False):
        print("   ❌ expose.html missing - required for Party Horn feature")
    if not found_files.get("explore.html", False):
        print("   ❌ explore.html missing - required for Speech Synthesis feature")
    if not found_files.get("expose.js", False):
        print("   ❌ expose.js missing - place your JavaScript in assets/scripts/expose.js")
    if not pages_working:
        print("   ❌ GitHub Pages not working - enable in Settings → Pages")
    if not has_actions:
        print("   ❌ GitHub Actions not configured - add .github/workflows/main.yml")
    
    # Confirm what WAS found
    print("\n✅ CORRECTLY DETECTED:")
    print(f"   • expose.html: {'PRESENT' if found_files.get('expose.html', False) else 'missing'}")
    print(f"   • explore.html: {'PRESENT' if found_files.get('explore.html', False) else 'missing'}")
    print(f"   • README.md: {'PRESENT' if found_files.get('README.md', False) else 'missing'}")
    
    print("\n" + "=" * 70)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 grade_student.py <github_repo_url>")
        print("Example: python3 grade_student.py https://github.com/phamhscott/Lab5_Starter")
        sys.exit(1)
    
    repo_url = sys.argv[1]
    scrape_student_repo(repo_url)

if __name__ == "__main__":
    main()