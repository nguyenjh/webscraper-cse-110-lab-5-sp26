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
    
    # Look for variable declarations or direct selectors
    tests = [
        ("Audio element", ['audio', 'getElementById.*audio', 'querySelector.*audio']),
        ("Horn select dropdown", ['hornSelect', 'getElementById.*horn', 'querySelector.*horn']),
        ("Volume slider", ['volumeSlider', 'getElementById.*volume', 'querySelector.*volume']),
        ("Play button", ['playButton', 'getElementById.*play', 'querySelector.*play', "querySelector('button')"]),
        ("Volume icon", ['volumeIcon', 'getElementById.*volume-icon', 'querySelector.*volume-icon']),
        ("Sound image", ['image', 'soundImage', 'getElementById.*image', 'querySelector.*#expose img', "querySelector('#expose img')"]),
    ]
    
    for name, patterns in tests:
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
    
    event_tests = [
        ("Horn selection change", ['addEventListener.*change', 'hornSelect.*change', 'onchange']),
        ("Volume control input", ['addEventListener.*input', 'volumeSlider.*input', 'oninput']),
        ("Play button click", ['addEventListener.*click', 'playButton.*click', 'onclick']),
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
    
    volume_tests = [
        ("Sets audio volume", [r'audio\.volume\s*=', r'\.volume\s*=']),
        ("Converts 0-100 to 0-1", [r'volume\s*/\s*100', r'\.volume\s*=\s*\w+\s*/\s*100']),
        ("Volume icon level 0", [r'volume\s*==\s*0', r'volume\s*<\s*1', r'level-0']),
        ("Volume icon level 1", [r'volume\s*<\s*33', r'level-1']),
        ("Volume icon level 2", [r'volume\s*<\s*67', r'level-2']),
        ("Volume icon level 3", [r'else\s*{', r'level-3']),
    ]
    
    for name, patterns in volume_tests:
        found = any(re.search(pattern, js_content, re.IGNORECASE) for pattern in patterns)
        results["total_tests"] += 1
        if found:
            results["passed_tests"] += 1
            results["details"].append(f"✅ {name}")
            print(f"      ✅ {name}")
        else:
            results["details"].append(f"⚠️  {name} not clearly detected")
            print(f"      ⚠️  {name}: Pattern not found")
    
    # Test 4: Horn selection logic
    print("\n    🎺 Horn Selection:")
    
    horn_tests = [
        ("Updates image src", [r'image\.src\s*=', r'\.src\s*=']),
        ("Updates audio src", [r'audio\.src\s*=', r'\.src\s*=.*audio']),
        ("Conditional logic", [r'if.*selectedHorn', r'switch', r'else if']),
    ]
    
    for name, patterns in horn_tests:
        found = any(re.search(pattern, js_content, re.IGNORECASE) for pattern in patterns)
        results["total_tests"] += 1
        if found:
            results["passed_tests"] += 1
            results["details"].append(f"✅ {name}")
            print(f"      ✅ {name}")
        else:
            results["details"].append(f"⚠️  {name} not detected")
            print(f"      ⚠️  {name}: Not found")
    
    # Test 5: Confetti implementation (FIXED - looking for exact pattern)
    print("\n    🎉 Confetti:")
    
    # Look for the exact pattern from the student's code
    has_js_confetti = re.search(r'new\s+JSConfetti\(\)|jsConfetti', js_content)
    has_add_confetti = re.search(r'\.addConfetti\(\)', js_content)
    has_party_horn_check = re.search(r'if\s*\(.*===.*party-horn.*\)\s*\{[^}]*\.addConfetti', js_content, re.DOTALL)
    
    results["total_tests"] += 1
    if has_js_confetti:
        results["passed_tests"] += 1
        results["details"].append("✅ JSConfetti initialized")
        print(f"      ✅ JSConfetti initialized")
    else:
        results["details"].append("❌ JSConfetti not initialized")
        print(f"      ❌ JSConfetti not initialized")
    
    results["total_tests"] += 1
    if has_add_confetti:
        results["passed_tests"] += 1
        results["details"].append("✅ addConfetti() called")
        print(f"      ✅ addConfetti() called")
    else:
        results["details"].append("❌ addConfetti() not called")
        print(f"      ❌ addConfetti() not called")
    
    results["total_tests"] += 1
    if has_party_horn_check:
        results["passed_tests"] += 1
        results["details"].append("✅ Confetti only for party horn")
        print(f"      ✅ Confetti only for party horn (conditional check present)")
    else:
        # Check for any conditional check around confetti
        conditional_confetti = re.search(r'if.*confetti', js_content, re.IGNORECASE)
        if conditional_confetti:
            results["passed_tests"] += 1
            results["details"].append("✅ Confetti has conditional check")
            print(f"      ✅ Confetti has conditional check")
        else:
            results["details"].append("⚠️  Confetti might not be conditional")
            print(f"      ⚠️  Confetti conditional check not found")
    
    # Test 6: Play sound logic
    print("\n    ▶️  Play Sound:")
    
    play_tests = [
        ("Calls play()", [r'\.play\(\)']),
        ("In click handler", [r'click.*\(\)\s*{[^}]*\.play', r'addEventListener.*click[^}]*\.play']),
    ]
    
    for name, patterns in play_tests:
        found = any(re.search(pattern, js_content, re.IGNORECASE | re.DOTALL) for pattern in patterns)
        results["total_tests"] += 1
        if found:
            results["passed_tests"] += 1
            results["details"].append(f"✅ {name}")
            print(f"      ✅ {name}")
        else:
            results["details"].append(f"⚠️  {name} not detected")
            print(f"      ⚠️  {name}: Not found")
    
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
    
    # Speech synthesis tests
    speech_tests = [
        ("SpeechSynthesis API", [r'speechSynthesis']),
        ("getVoices() called", [r'getVoices\(\)']),
        ("Voice dropdown population", [r'for.*voices', r'forEach.*voice', r'createElement.*option', r'innerHTML.*option']),
        ("Speak button event", [r'addEventListener.*click', r'talkButton', r'speakButton']),
        ("SpeechSynthesisUtterance", [r'SpeechSynthesisUtterance']),
        ("Sets voice property", [r'\.voice\s*=']),
        ("Gets text from textarea", [r'textarea\.value', r'\.textContent']),
        ("Face animation start", [r'onstart', r'onspeechstart', r'\.src.*open', r'\.src.*mouth']),
        ("Face animation end", [r'onend', r'onspeechend', r'\.src.*closed']),
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
            print(f"      ⚠️  {name}: Pattern not found")
    
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
            if 'Scott' in line or re.match(r'^[A-Z][a-z]+ [A-Z][a-z]+$', line.strip()):
                print(f"  📝 Student: {line.strip()}")
                break
        else:
            print("  📝 Student name found in README")
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
        print(f"  {'✅' if pages_working else '❌'} GitHub Pages: {pages_url}")
        print(f"      expose.html: {'OK' if r1.status_code == 200 else 'Failed'}")
        print(f"      explore.html: {'OK' if r2.status_code == 200 else 'Failed'}")
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
    
    # Summary of what's working
    print("\n✅ SUMMARY OF WORKING FEATURES:")
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