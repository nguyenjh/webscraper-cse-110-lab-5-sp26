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
    Simple direct pattern matching for actual code.
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
    
    # Simple checks for element selections
    selector_tests = [
        ("Audio element", ['audio', 'hornSound', 'sound']),
        ("Horn select dropdown", ['select', 'hornSelect', 'horn-select']),
        ("Volume slider", ['slider', 'volumeSlider', 'volume']),
        ("Play button", ['button', 'playButton', 'play']),
        ("Volume icon", ['volumeImage', 'volumeImg', 'volumeIcon', 'volume-image']),
        ("Sound/Horn image", ['hornImage', 'hornImg', 'image']),
    ]
    
    for name, patterns in selector_tests:
        found = any(re.search(rf'\b{pattern}\b', js_content, re.IGNORECASE) for pattern in patterns)
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
    
    event_tests = [
        ("Horn selection change", ['change', 'addEventListener.*change']),
        ("Volume control input", ['input', 'addEventListener.*input']),
        ("Play button click", ['click', 'addEventListener.*click']),
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
    
    # Look for volume-related code
    has_volume_assignment = re.search(r'\.volume\s*=', js_content)
    has_volume_calculation = re.search(r'volume\s*/\s*100', js_content)
    has_volume_conditions = re.search(r'if\s*\([^)]*volume[^)]*\)', js_content)
    has_volume_icons = re.search(r'volumeImage\.src\s*=|volumeImg\.src\s*=|volumeIcon\.src\s*=', js_content)
    has_level0 = re.search(r'volume-level-0\.svg', js_content)
    has_level1 = re.search(r'volume-level-1\.svg', js_content)
    has_level2 = re.search(r'volume-level-2\.svg', js_content)
    has_level3 = re.search(r'volume-level-3\.svg', js_content)
    
    results["total_tests"] += 1
    if has_volume_assignment:
        results["passed_tests"] += 1
        print(f"      ✅ Sets audio volume property")
    else:
        print(f"      ❌ Sets audio volume property not found")
    
    results["total_tests"] += 1
    if has_volume_calculation:
        results["passed_tests"] += 1
        print(f"      ✅ Converts volume from 0-100 to 0-1")
    else:
        print(f"      ⚠️  Volume conversion not clearly detected")
    
    results["total_tests"] += 1
    if has_volume_icons and has_level0:
        results["passed_tests"] += 1
        print(f"      ✅ Volume icon updates with different levels")
    else:
        print(f"      ❌ Volume icon updates not found")
    
    # Test 4: Horn selection logic
    print("\n    🎺 Horn Selection:")
    
    # Look for image and audio updates
    has_image_update = re.search(r'(hornImage|hornImg)\.src\s*=', js_content) or re.search(r'\.src\s*=\s*[\'"]assets/images/', js_content)
    has_audio_update = re.search(r'(hornSound|audio)\.src\s*=', js_content) or re.search(r'\.src\s*=\s*[\'"]assets/audio/', js_content)
    has_conditional = re.search(r'else\s+if|switch', js_content)
    
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
    
    has_js_confetti = re.search(r'new\s+JSConfetti\(\)', js_content)
    has_add_confetti = re.search(r'\.addConfetti\(\)', js_content)
    
    # Look for party horn condition in click handler
    click_handler_match = re.search(r'addEventListener\([\'"]click[\'"]\s*,\s*\([^)]*\)\s*=>?\s*\{([^}]*)\}', js_content, re.DOTALL)
    has_party_check = False
    
    if click_handler_match:
        handler_body = click_handler_match.group(1)
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
        print(f"      ✅ Confetti only for party horn")
    else:
        # Also check if there's any conditional around confetti
        if re.search(r'if\s*\([^)]*\)\s*\{[^}]*addConfetti', js_content, re.DOTALL):
            results["passed_tests"] += 1
            print(f"      ✅ Confetti has conditional check")
        else:
            print(f"      ❌ Confetti not conditionally checked")
    
    # Test 6: Play sound logic
    print("\n    ▶️  Play Sound:")
    
    has_play_call = re.search(r'\.play\(\)', js_content)
    has_src_check = re.search(r'if\s*\([^)]*src[^)]*\)\s*\{[^}]*\.play', js_content, re.DOTALL)
    
    results["total_tests"] += 1
    if has_play_call:
        results["passed_tests"] += 1
        print(f"      ✅ Calls play() method")
    else:
        print(f"      ❌ Calls play() method not found")
    
    results["total_tests"] += 1
    if has_src_check:
        results["passed_tests"] += 1
        print(f"      ✅ Checks if source exists before playing")
    else:
        print(f"      ⚠️  No source check detected (optional)")
        # Don't deduct points for this
        results["total_tests"] -= 1
    
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
        # Look for common name patterns
        lines = readme.split('\n')[:15]
        for line in lines:
            # Look for "Name: Scott Pham" pattern
            name_match = re.search(r'^[*]?name[*]?\s*:\s*(.+)$', line, re.IGNORECASE)
            if name_match:
                print(f"  📝 Student: {name_match.group(1).strip()}")
                break
            # Look for standalone name at beginning
            if re.match(r'^[A-Z][a-z]+ [A-Z][a-z]+$', line.strip()):
                if line.strip() not in ["About", "Resources", "Activity"]:
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
    print(f"  📈 Documentation & Files: {docs_score*100:.1f}%")
    print(f"  📈 GitHub Pages: {'100%' if pages_working else '0%'}")
    
    print(f"\n  {'='*50}")
    print(f"  🎓 FINAL GRADE: {final_grade:.1f}%")
    print(f"  {'='*50}")
    
    # Show what's working
    print("\n✅ CORRECTLY IMPLEMENTED FEATURES:")
    for detail in expose_results["details"]:
        if "✅" in detail:
            print(f"  • {detail}")
    
    # Provide feedback if needed
    if expose_score > 0.8:
        print("\n🎉 Great job! The Party Horn implementation looks correct!")
    
    print("\n" + "=" * 80)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <github_repo_url>")
        print("Example: python3 main.py https://github.com/phamhscott/Lab5_Starter")
        sys.exit(1)
    
    grade_submission(sys.argv[1])

if __name__ == "__main__":
    main()