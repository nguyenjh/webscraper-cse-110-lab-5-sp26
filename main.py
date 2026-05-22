#!/usr/bin/env python3
import sys
import requests
import re
from typing import Dict, List, Any

def parse_repo_url(url):
    """Extract owner and repo name from GitHub URL."""
    if "github.com" in url:
        parts = url.rstrip('/').split('/')
        owner = parts[-2]
        repo = parts[-1]
    else:
        owner, repo = url.split('/')[-2:]
    return owner, repo

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

def test_expose_javascript(js_content: str) -> Dict[str, Any]:
    """
    Test the expose.js implementation for Party Horn requirements.
    Uses semantic analysis rather than strict string matching.
    """
    results = {
        "total_tests": 0,
        "passed_tests": 0,
        "details": []
    }
    
    if not js_content:
        results["details"].append("❌ No JavaScript content found")
        return results
    
    print("\n  🔍 Testing expose.js implementation:")
    
    # Test 1: DOM element selectors - Look for variable declarations
    print("\n    📌 DOM Element Selectors:")
    
    # Check for element selections (any form)
    has_select = re.search(r'(const|let|var)\s+(\w+)\s*=\s*document\.(querySelector|getElementById)', js_content)
    has_audio = re.search(r'(const|let|var)\s+(\w+)\s*=\s*document\.querySelector\([\'"]audio[\'"]\)', js_content)
    has_button = re.search(r'(const|let|var)\s+(\w+)\s*=\s*document\.querySelector\([\'"]button[\'"]\)', js_content)
    has_slider = re.search(r'(const|let|var)\s+(\w+)\s*=\s*document\.querySelector\([\'"]input[\'"]\)', js_content)
    
    # Track what variables are used for what
    var_names = {}
    for match in re.finditer(r'(const|let|var)\s+(\w+)\s*=\s*document\.(querySelector|getElementById)\([\'"]([^\'"]+)[\'"]\)', js_content):
        var_names[match.group(2)] = match.group(4)
    
    print(f"      Variables detected: {var_names}")
    
    selector_tests = [
        ("Audio element", [r'document\.querySelector\([\'"]audio', r'const\s+\w+\s*=\s*document\.querySelector\([\'"]audio']),
        ("Horn select dropdown", [r'document\.querySelector\([\'"]select', r'const\s+\w+\s*=\s*document\.querySelector\([\'"]select']),
        ("Volume slider", [r'document\.querySelector\([\'"]input', r'const\s+\w+\s*=\s*document\.querySelector\([\'"]input']),
        ("Play button", [r'document\.querySelector\([\'"]button', r'const\s+\w+\s*=\s*document\.querySelector\([\'"]button']),
        ("Volume icon", [r'volumeImg', r'volumeIcon', r'querySelector.*\[alt.*volume']),
        ("Sound/Horn image", [r'hornImg', r'soundImage', r'querySelector.*\[alt.*image']),
    ]
    
    for name, patterns in selector_tests:
        found = any(re.search(pattern, js_content, re.IGNORECASE) for pattern in patterns)
        results["total_tests"] += 1
        if found:
            results["passed_tests"] += 1
            results["details"].append(f"✅ {name} selector found")
            print(f"      ✅ {name}: Found")
        else:
            results["details"].append(f"❌ {name} selector missing")
            print(f"      ❌ {name}: Not found")
    
    # Test 2: Event listeners
    print("\n    🎯 Event Listeners:")
    
    # Look for addEventListener calls
    event_listeners = re.findall(r'\.addEventListener\([\'"]([^\'"]+)[\'"]', js_content)
    print(f"      Events detected: {event_listeners}")
    
    event_tests = [
        ("Horn selection change", [r'addEventListener\([\'"]change[\'"]', r'select\.addEventListener']),
        ("Volume control input", [r'addEventListener\([\'"]input[\'"]', r'slider\.addEventListener']),
        ("Play button click", [r'addEventListener\([\'"]click[\'"]', r'button\.addEventListener']),
    ]
    
    for name, patterns in event_tests:
        found = any(re.search(pattern, js_content, re.IGNORECASE) for pattern in patterns)
        results["total_tests"] += 1
        if found:
            results["passed_tests"] += 1
            results["details"].append(f"✅ {name} event listener")
            print(f"      ✅ {name}: Found")
        else:
            results["details"].append(f"❌ {name} event listener missing")
            print(f"      ❌ {name}: Not found")
    
    # Test 3: Volume logic
    print("\n    🔊 Volume Control:")
    
    # Look for audio volume being set
    has_volume_assignment = re.search(r'\w+\.volume\s*=', js_content)
    has_volume_calculation = re.search(r'volume\s*/\s*\w+|\.volume\s*=\s*\w+\s*/\s*\w+', js_content)
    
    # Look for volume level conditions
    has_level_conditions = re.search(r'if\s*\([^)]*volume[^)]*\)', js_content)
    has_multiple_levels = len(re.findall(r'else\s+if|else\s*\{', js_content)) >= 3
    
    # Look for volume icon updates
    has_icon_updates = re.search(r'volumeImg\.src\s*=|volumeIcon\.src\s*=', js_content)
    
    results["total_tests"] += 1
    if has_volume_assignment:
        results["passed_tests"] += 1
        print(f"      ✅ Sets audio volume property")
    else:
        print(f"      ❌ Sets audio volume property not found")
    
    results["total_tests"] += 1
    if has_volume_calculation:
        results["passed_tests"] += 1
        print(f"      ✅ Converts volume range")
    else:
        print(f"      ⚠️  Volume conversion not clearly detected")
    
    results["total_tests"] += 1
    if has_level_conditions and has_multiple_levels:
        results["passed_tests"] += 1
        print(f"      ✅ Multiple volume level conditions")
    else:
        print(f"      ⚠️  Volume conditions detected but may be incomplete")
        if has_level_conditions:
            results["passed_tests"] += 1  # Give partial credit
    
    results["total_tests"] += 1
    if has_icon_updates:
        results["passed_tests"] += 1
        print(f"      ✅ Volume icon updates")
    else:
        print(f"      ❌ Volume icon updates not found")
    
    # Test 4: Horn selection logic - FIXED: Look for ANY src assignment in the change handler
    print("\n    🎺 Horn Selection:")
    
    # Find the change handler body
    change_handler = re.search(r'addEventListener\([\'"]change[\'"]\s*,\s*\([^)]*\)\s*=>?\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}', js_content, re.DOTALL)
    
    has_image_update = False
    has_audio_update = False
    
    if change_handler:
        handler_body = change_handler.group(1)
        # Look for any .src assignment to an image-related variable
        has_image_update = re.search(r'\w+\.src\s*=', handler_body)
        # Look for any .src assignment to audio
        has_audio_update = re.search(r'(audio|sound)\w*\.src\s*=', handler_body, re.IGNORECASE)
    
    # Also check for switch/case statements
    has_switch = re.search(r'switch\s*\([^)]*\)\s*{', js_content)
    has_cases = re.search(r'case\s+[\'"]?(air|car|party)-horn', js_content)
    
    results["total_tests"] += 1
    if has_image_update:
        results["passed_tests"] += 1
        print(f"      ✅ Updates horn image (.src assignment detected)")
    else:
        # Check for image updates anywhere
        if re.search(r'hornImg\.src\s*=', js_content):
            results["passed_tests"] += 1
            print(f"      ✅ Updates horn image")
        else:
            print(f"      ❌ Updates horn image not found")
    
    results["total_tests"] += 1
    if has_audio_update:
        results["passed_tests"] += 1
        print(f"      ✅ Updates audio source (.src assignment detected)")
    else:
        # Check for audio updates anywhere
        if re.search(r'audio\.src\s*=', js_content):
            results["passed_tests"] += 1
            print(f"      ✅ Updates audio source")
        else:
            print(f"      ❌ Updates audio source not found")
    
    results["total_tests"] += 1
    if has_switch or has_cases:
        results["passed_tests"] += 1
        print(f"      ✅ Conditional logic (switch/case) for different horns")
    else:
        print(f"      ⚠️  Conditional logic detected but not switch/case")
        if re.search(r'if.*else', js_content):
            results["passed_tests"] += 1
    
    # Test 5: Confetti implementation
    print("\n    🎉 Confetti:")
    
    has_js_confetti = re.search(r'new\s+JSConfetti\(\)', js_content)
    has_add_confetti = re.search(r'\.addConfetti\(\)', js_content)
    
    # Look for confetti in click handler with party horn condition
    click_handler = re.search(r'addEventListener\([\'"]click[\'"]\s*,\s*\([^)]*\)\s*=>?\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}', js_content, re.DOTALL)
    has_party_check = False
    
    if click_handler:
        handler_body = click_handler.group(1)
        has_party_check = re.search(r'if\s*\([^)]*party-horn[^)]*\)\s*\{[^}]*addConfetti', handler_body, re.DOTALL)
    
    results["total_tests"] += 1
    if has_js_confetti:
        results["passed_tests"] += 1
        print(f"      ✅ JSConfetti initialized")
    else:
        print(f"      ❌ JSConfetti not initialized")
    
    results["total_tests"] += 1
    if has_add_confetti:
        results["passed_tests"] += 1
        print(f"      ✅ addConfetti() called")
    else:
        print(f"      ❌ addConfetti() not called")
    
    results["total_tests"] += 1
    if has_party_check:
        results["passed_tests"] += 1
        print(f"      ✅ Confetti only for party horn (conditional check)")
    else:
        # Check for any conditional around confetti
        if re.search(r'if\s*\([^)]*\)\s*\{[^}]*addConfetti', js_content, re.DOTALL):
            results["passed_tests"] += 1
            print(f"      ✅ Confetti has conditional check")
        else:
            print(f"      ❌ Confetti not conditionally checked")
    
    # Test 6: Play sound logic
    print("\n    ▶️  Play Sound:")
    
    has_play_call = re.search(r'\.play\(\)', js_content)
    has_prevention = re.search(r'if\s*\([^)]*src[^)]*\)\s*\{[^}]*\.play', js_content, re.DOTALL)
    
    results["total_tests"] += 1
    if has_play_call:
        results["passed_tests"] += 1
        print(f"      ✅ Calls play() method")
    else:
        print(f"      ❌ Calls play() method not found")
    
    results["total_tests"] += 1
    if has_prevention:
        results["passed_tests"] += 1
        print(f"      ✅ Prevents playing when no sound selected")
    else:
        print(f"      ⚠️  No play prevention detected (optional)")
    
    return results

def test_explore_javascript(js_content: str) -> Dict[str, Any]:
    """
    Test the explore.js implementation for Speech Synthesis requirements.
    """
    results = {
        "total_tests": 0,
        "passed_tests": 0,
        "details": []
    }
    
    if not js_content:
        results["details"].append("⚠️  No explore.js content found")
        return results
    
    if len(js_content.strip()) == 0:
        results["details"].append("⚠️  explore.js is empty")
        return results
    
    print("\n  🔍 Testing explore.js implementation:")
    
    speech_tests = [
        ("SpeechSynthesis API", [r'speechSynthesis']),
        ("getVoices() called", [r'getVoices\(\)']),
        ("Voice dropdown", [r'createElement.*option', r'innerHTML.*option', r'for.*voices']),
        ("Speak button event", [r'addEventListener.*click', r'talk.*click']),
        ("SpeechSynthesisUtterance", [r'SpeechSynthesisUtterance']),
        ("Sets voice", [r'\.voice\s*=']),
        ("Gets text", [r'textarea\.value', r'\.textContent']),
        ("Face animation", [r'\.src.*open', r'\.src.*closed', r'onstart', r'onend']),
    ]
    
    for name, patterns in speech_tests:
        found = any(re.search(pattern, js_content, re.IGNORECASE) for pattern in patterns)
        results["total_tests"] += 1
        if found:
            results["passed_tests"] += 1
            results["details"].append(f"✅ {name}")
            print(f"      ✅ {name}")
        else:
            results["details"].append(f"⚠️  {name} not detected")
            print(f"      ⚠️  {name}: Not found")
    
    return results

def grade_submission(repo_url):
    """Main grading function."""
    print("=" * 80)
    print(f"🎓 GRADING STUDENT SUBMISSION")
    print(f"   {repo_url}")
    print("=" * 80)
    
    owner, repo = parse_repo_url(repo_url)
    print(f"\n📂 Repository: {owner}/{repo}")
    
    # Fetch files
    print("\n📥 Fetching files...")
    
    expose_js = get_file_content(owner, repo, "assets/scripts/expose.js")
    explore_js = get_file_content(owner, repo, "assets/scripts/explore.js")
    readme = get_file_content(owner, repo, "README.md")
    
    files_status = {
        "expose.html": get_file_content(owner, repo, "expose.html"),
        "explore.html": get_file_content(owner, repo, "explore.html"),
        "expose.js": expose_js,
        "explore.js": explore_js,
        "README.md": readme,
        "package.json": get_file_content(owner, repo, "package.json"),
        "unit.test.js": get_file_content(owner, repo, "__tests__/unit.test.js"),
        "main.yml": get_file_content(owner, repo, ".github/workflows/main.yml"),
    }
    
    for name, content in files_status.items():
        print(f"  {'✅' if content else '❌'} {name}")
    
    # Extract student name
    print("\n👥 Student Information:")
    if readme:
        lines = readme.split('\n')[:10]
        for line in lines:
            if re.search(r'[A-Z][a-z]+ [A-Z][a-z]+', line):
                names = re.findall(r'[A-Z][a-z]+ [A-Z][a-z]+', line)
                if names:
                    print(f"  📝 Student: {names[0]}")
                    break
        else:
            print("  📝 Student name present in README")
    
    # Test expose.js
    print("\n" + "=" * 80)
    print("🎯 PART 1: TESTING expose.js (Party Horn)")
    print("=" * 80)
    
    expose_results = test_expose_javascript(expose_js)
    
    # Test explore.js
    print("\n" + "=" * 80)
    print("🗣️  PART 2: TESTING explore.js (Speech Synthesis)")
    print("=" * 80)
    
    explore_results = test_explore_javascript(explore_js)
    
    # Check GitHub Pages
    print("\n" + "=" * 80)
    print("🌐 PART 3: GITHUB PAGES")
    print("=" * 80)
    
    pages_url = f"https://{owner}.github.io/{repo}"
    expose_url = f"{pages_url}/expose.html"
    explore_url = f"{pages_url}/explore.html"
    
    try:
        r1 = requests.get(expose_url, timeout=5)
        r2 = requests.get(explore_url, timeout=5)
        pages_working = r1.status_code == 200 and r2.status_code == 200
        print(f"  ✅ GitHub Pages deployed: {pages_url}")
        print(f"      expose.html: {r1.status_code}")
        print(f"      explore.html: {r2.status_code}")
    except:
        print(f"  ❌ GitHub Pages not accessible")
        pages_working = False
    
    # Check screenshots
    print("\n" + "=" * 80)
    print("📸 PART 4: SCREENSHOTS")
    print("=" * 80)
    
    error_screenshot = get_file_content(owner, repo, "myError.png")
    merge_screenshot = get_file_content(owner, repo, "merged.png")
    
    print(f"  {'✅' if error_screenshot else '❌'} myError.png")
    print(f"  {'✅' if merge_screenshot else '❌'} merged.png")
    
    # Calculate final grade
    print("\n" + "=" * 80)
    print("📊 FINAL GRADE")
    print("=" * 80)
    
    expose_score = expose_results["passed_tests"] / expose_results["total_tests"] if expose_results["total_tests"] > 0 else 0
    explore_score = explore_results["passed_tests"] / explore_results["total_tests"] if explore_results["total_tests"] > 0 else 0
    
    # Documentation score
    docs_score = sum([
        1 if files_status["README.md"] else 0,
        1 if files_status["package.json"] else 0,
        1 if files_status["unit.test.js"] else 0,
        1 if files_status["main.yml"] else 0,
        1 if error_screenshot else 0,
        1 if merge_screenshot else 0,
    ]) / 6
    
    # Weighted grade
    final_grade = (expose_score * 0.45 + explore_score * 0.30 + docs_score * 0.15 + (0.1 if pages_working else 0)) * 100
    
    print(f"\n  📈 expose.js: {expose_score*100:.1f}% ({expose_results['passed_tests']}/{expose_results['total_tests']} tests)")
    print(f"  📈 explore.js: {explore_score*100:.1f}% ({explore_results['passed_tests']}/{explore_results['total_tests']} tests)")
    print(f"  📈 Documentation: {docs_score*100:.1f}%")
    print(f"  📈 GitHub Pages: {'100%' if pages_working else '0%'}")
    
    print(f"\n  {'='*50}")
    print(f"  🎓 FINAL GRADE: {final_grade:.1f}%")
    print(f"  {'='*50}")
    
    # Summary
    print("\n✅ WHAT'S WORKING:")
    for detail in expose_results["details"]:
        if "✅" in detail:
            print(f"  {detail}")
    
    print("\n" + "=" * 80)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <github_repo_url>")
        print("Example: python3 main.py https://github.com/phamhscott/Lab5_Starter")
        sys.exit(1)
    
    grade_submission(sys.argv[1])

if __name__ == "__main__":
    main()