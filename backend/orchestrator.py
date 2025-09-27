import json
import subprocess
import os
import shutil
import platform
import sys
import datetime

from .report import generate_html_report
from .logger import log_error  # optional: if you want to log errors separately

CATALOG = os.path.join(os.path.dirname(__file__), "tests_catalog.json")
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Detect OS
if len(sys.argv) > 1:
    SELECTED_OS = sys.argv[1].lower()
else:
    SELECTED_OS = platform.system().lower()  # "windows" or "linux"


def run_script(item, use_fix=False):
    """Run either a check script or a fix script depending on use_fix flag."""
    s = item['fix'] if use_fix else item['check']
    script = s['script']
    script_path = os.path.abspath(os.path.join(PROJECT_ROOT, script))

    if not os.path.exists(script_path):
        return 1, "", f"Script not found: {script_path}"

    if item.get("os") and item["os"].lower() != SELECTED_OS:
        return 0, f"Skipped: {item['os']} check on {SELECTED_OS}", f"Skipped: {item['os']} check on {SELECTED_OS}"

    if s['type'] == 'powershell':
        if shutil.which("pwsh"):
            cmd = ["pwsh", "-ExecutionPolicy", "Bypass", "-File", script_path]
        else:
            cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path]
    elif s['type'] == 'bash':
        if SELECTED_OS != "linux":
            return 0, f"Skipped: linux check on {SELECTED_OS}", f"Skipped: linux check on {SELECTED_OS}"
        cmd = ["/bin/bash", script_path]
    else:
        return 1, "", f"Unknown script type {s['type']}"

    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def run_fix(test_id):
    """Run the fix for a given test_id if available."""
    try:
        with open(CATALOG) as f:
            tests = json.load(f)
        for t in tests:
            if t.get("id") == test_id and "fix" in t:
                rc, out, err = run_script(t, use_fix=True)
                return {
                    "id": t["id"],
                    "title": t["title"],
                    "rc": rc,
                    "out": out if out else err,
                    "err": err,
                    "fix_description": t.get("fix_description", ""),
                    "os": t.get("os", "").lower()
                }
    except Exception as e:
        log_error(f"Error running fix for {test_id}: {e}")
    return {"id": test_id, "error": "No fix available for this test."}


def main():
    try:
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
                "has_fix": "fix" in t,
                "fix_description": t.get("fix_description", ""),
                "os": t.get("os", "").lower()  # important for report filtering
            })

        # Generate HTML report
        generate_html_report(results, SELECTED_OS)

        # Only output JSON to stdout for GUI
        print(json.dumps(results, indent=2))

    except Exception:
        import traceback
        log_file = log_error(traceback.format_exc())
        print(f'{{"error": "Unexpected error occurred. See log: {log_file}"}}')


if __name__ == "__main__":
    main()
