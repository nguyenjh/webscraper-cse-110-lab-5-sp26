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
    
    # Test 1: DOM element selectors
    print("\n    📌 DOM Element Selectors:")
    
    # Check for various selector patterns
    has_audio = bool(re.search(r'document\.querySelector\([\'"]audio[\'"]\)|const\s+audio\s*=', js_content))
    has_dropdown = bool(re.search(r'document\.querySelector\([\'"]?#horn-select[\'"]\)|const\s+dropdown\s*=', js_content))
    has_volume_control = bool(re.search(r'document\.querySelector\([\'"]?#volume-controls input[\'"]\)|volumeControl', js_content))
    has_play_button = bool(re.search(r'document\.querySelector\([\'"]button[\'"]\)|playButton', js_content))
    has_volume_icon = bool(re.search(r'document\.querySelector\([\'"]?#volume-controls img[\'"]\)|horn\s*=', js_content))
    has_horn_image = bool(re.search(r'document\.querySelector\([\'"]img[\'"]\)|image\s*=', js_content))
    
    selector_results = [
        ("Audio element", has_audio),
        ("Horn select dropdown", has_dropdown),
        ("Volume slider", has_volume_control),
        ("Play button", has_play_button),
        ("Volume icon", has_volume_icon),
        ("Sound/Horn image", has_horn_image),
    ]
    
    for name, found in selector_results:
        results["total_tests"] += 1
        if found:
            results["passed_tests"] += 1
            results["details"].append(f"✅ {name} selector found")
            print(f"      ✅ {name}: Found")
        else:
            results["details"].append(f"⚠️  {name} selector not explicitly found")
            print(f"      ⚠️  {name}: Not explicitly found")
    
    # Test 2: Event listeners
    print("\n    🎯 Event Listeners:")
    
    has_change = bool(re.search(r'addEventListener\([\'"]change[\'"]', js_content))
    has_input = bool(re.search(r'addEventListener\([\'"]input[\'"]', js_content))
    has_click = bool(re.search(r'addEventListener\([\'"]click[\'"]', js_content))
    
    event_results = [
        ("Horn selection change", has_change),
        ("Volume control input", has_input),
        ("Play button click", has_click),
    ]
    
    for name, found in event_results:
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
    
    has_volume_assignment = bool(re.search(r'audio\.volume\s*=', js_content))
    has_volume_conversion = bool(re.search(r'volumeControl\.value\s*/\s*100', js_content))
    has_volume_conditions = bool(re.search(r'if\s*\([^)]*volumeControl\.value[^)]*\)', js_content))
    
    # Look for ANY src assignment that points to volume-level SVG files
    has_volume_icons = bool(re.search(r'\.src\s*=\s*[\'"]assets/icons/volume-level-[0-3]\.svg[\'"]', js_content))
    
    # Count how many volume levels are present
    volume_levels = re.findall(r'volume-level-([0-3])\.svg', js_content)
    has_multiple_levels = len(set(volume_levels)) >= 3
    
    results["total_tests"] += 1
    if has_volume_assignment:
        results["passed_tests"] += 1
        print(f"      ✅ Sets audio volume property")
    else:
        print(f"      ❌ Sets audio volume property not found")
    
    results["total_tests"] += 1
    if has_volume_conversion:
        results["passed_tests"] += 1
        print(f"      ✅ Converts volume from 0-100 to 0-1")
    else:
        print(f"      ⚠️  Volume conversion not clearly detected")
    
    results["total_tests"] += 1
    if has_volume_conditions and has_volume_icons:
        results["passed_tests"] += 1
        print(f"      ✅ Volume icon updates with different levels")
    elif has_volume_icons:
        results["passed_tests"] += 1
        print(f"      ✅ Volume icon updates detected")
    else:
        print(f"      ❌ Volume icon updates not found")
    
    # Test 4: Horn selection logic
    print("\n    🎺 Horn Selection:")
    
    # Look for image src updates with template literals or string concatenation
    has_image_update = bool(re.search(r'image\.src\s*=\s*`[^`]*\${[^}]+}[^`]*`|\.src\s*=\s*[\'"]assets/images/', js_content))
    has_audio_update = bool(re.search(r'audio\.src\s*=\s*`[^`]*\${[^}]+}[^`]*`|\.src\s*=\s*[\'"]assets/audio/', js_content))
    has_conditional = bool(re.search(r'else\s+if|switch', js_content))
    
    results["total_tests"] += 1
    if has_image_update:
        results["passed_tests"] += 1
        print(f"      ✅ Updates horn image")
    else:
        print(f"      ❌ Updates horn image not found")
    
    results["total_tests"] += 1
    if has_audio_update:
        results["passed_tests"] += 1
        print(f"      ✅ Updates audio source")
    else:
        print(f"      ❌ Updates audio source not found")
    
    results["total_tests"] += 1
    if has_conditional:
        results["passed_tests"] += 1
        print(f"      ✅ Conditional logic for different horns")
    else:
        print(f"      ⚠️  Conditional logic not clearly detected")
    
    # Test 5: Confetti implementation
    print("\n    🎉 Confetti:")
    
    has_js_confetti = bool(re.search(r'new\s+JSConfetti\(\)', js_content))
    has_add_confetti = bool(re.search(r'\.addConfetti\(\)', js_content))
    
    # Look for party horn condition
    has_party_check = bool(re.search(r'if\s*\([^)]*dropdown\.value\s*==\s*[\'"]party-horn[\'"]\)', js_content))
    
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
        print(f"      ✅ Confetti only for party horn")
    else:
        # Check for any conditional around confetti
        if re.search(r'if\s*\([^)]*\)\s*\{[^}]*addConfetti', js_content, re.DOTALL):
            results["passed_tests"] += 1
            print(f"      ✅ Confetti has conditional check")
        else:
            print(f"      ❌ Confetti not conditionally checked")
    
    # Test 6: Play sound logic
    print("\n    ▶️  Play Sound:")
    
    has_play_call = bool(re.search(r'\.play\(\)', js_content))
    
    results["total_tests"] += 1
    if has_play_call:
        results["passed_tests"] += 1
        print(f"      ✅ Calls play() method")
    else:
        print(f"      ❌ Calls play() method not found")
    
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
        ("Voice dropdown population", [r'createElement.*option', r'innerHTML.*option', r'for.*voices']),
        ("Speak button event", [r'addEventListener.*click', r'talkButton']),
        ("SpeechSynthesisUtterance", [r'SpeechSynthesisUtterance']),
        ("Sets voice property", [r'\.voice\s*=']),
        ("Gets text from textarea", [r'textarea\.value', r'\.value']),
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
        lines = readme.split('\n')[:15]
        for line in lines:
            name_match = re.search(r'^[*]?name[*]?\s*:\s*(.+)$', line, re.IGNORECASE)
            if name_match:
                print(f"  📝 Student: {name_match.group(1).strip()}")
                break
            if re.match(r'^[A-Z][a-z]+ [A-Z][a-z]+$', line.strip()):
                if line.strip() not in ["About", "Resources", "Activity", "Lab"]:
                    print(f"  📝 Student: {line.strip()}")
                    break
        else:
            print("  📝 Student name present in README")
    else:
        print("  ❌ No README found")
    
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
        print(f"      expose.html: {r1.status_code} OK")
        print(f"      explore.html: {r2.status_code} OK")
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
    docs_items = [
        files_status["README.md"],
        files_status["package.json"],
        files_status["unit.test.js"],
        files_status["main.yml"],
        error_screenshot,
        merge_screenshot,
    ]
    docs_score = sum(1 for item in docs_items if item) / len(docs_items)
    
    # Weighted grade
    final_grade = (expose_score * 0.45 + explore_score * 0.30 + docs_score * 0.15 + (0.1 if pages_working else 0)) * 100
    
    print(f"\n  📈 expose.js: {expose_score*100:.1f}% ({expose_results['passed_tests']}/{expose_results['total_tests']} tests)")
    print(f"  📈 explore.js: {explore_score*100:.1f}% ({explore_results['passed_tests']}/{explore_results['total_tests']} tests)")
    print(f"  📈 Documentation: {docs_score*100:.1f}%")
    print(f"  📈 GitHub Pages: {'100%' if pages_working else '0%'}")
    
    print(f"\n  {'='*50}")
    print(f"  🎓 FINAL GRADE: {final_grade:.1f}%")
    print(f"  {'='*50}")
    
    # Show what's working
    print("\n✅ CORRECTLY IMPLEMENTED FEATURES:")
    for detail in expose_results["details"]:
        if "✅" in detail:
            print(f"  • {detail}")
    
    # Provide summary feedback
    print("\n📝 SUMMARY:")
    if expose_score >= 0.9:
        print("  🎉 Excellent! All Party Horn features are working correctly!")
    elif expose_score >= 0.7:
        print("  👍 Good job! Most features are implemented correctly.")
    else:
        print("  ⚠️ Some features need to be reviewed.")
    
    print("\n" + "=" * 80)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <github_repo_url>")
        print("Example: python3 main.py https://github.com/phamhscott/Lab5_Starter")
        sys.exit(1)
    
    grade_submission(sys.argv[1])

if __name__ == "__main__":
    main()