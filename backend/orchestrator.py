import json
import subprocess
import os
import shutil
import platform
import sys
from report import generate_html_report  # import report generator

CATALOG = "backend/tests_catalog.json"
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Get OS from argument (optional), else detect current OS
if len(sys.argv) > 1:
    SELECTED_OS = sys.argv[1].lower()
else:
    SELECTED_OS = platform.system().lower()  # "windows" or "linux"

def run_script(item):
    s = item['check']
    script = s['script']
    script_path = os.path.abspath(os.path.join(PROJECT_ROOT, script))

    if not os.path.exists(script_path):
        return 1, "", f"Script not found: {script_path}"

    item_os = item.get("os")
    if item_os and item_os.lower() != SELECTED_OS:
        return 0, "", f"Skipped: {item_os} check on {SELECTED_OS}"

    if s['type'] == 'powershell':
        if shutil.which("pwsh"):
            cmd = ["pwsh", "-ExecutionPolicy", "Bypass", "-File", script_path]
        else:
            cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path]
    elif s['type'] == 'bash':
        if SELECTED_OS != "linux":
            return 0, "", f"Skipped: linux check on {SELECTED_OS}"
        cmd = ["/bin/bash", script_path]
    else:
        return 1, "", f"Unknown script type {s['type']}"

    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()

def main():
    with open(CATALOG) as f:
        tests = json.load(f)

    results = []
    for t in tests:
        rc, out, err = run_script(t)
        results.append({
            "id": t.get("id"),
            "title": t.get("title"),
            "rc": rc,
            "out": out if out else err,
            "err": err,
            "os": t.get("os", "unknown")  # <--- ensure OS field is always present
        })

    print(json.dumps(results, indent=2))

    # call the HTML report generator at the end
    generate_html_report(results, SELECTED_OS)

if __name__ == "__main__":
    main()
