import json, subprocess, os, shutil

CATALOG = "backend/tests_catalog.json"

# get project root (one level up from backend/)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def run_script(item):
    s = item['check']
    script = s['script']

    # resolve path relative to project root
    script_path = os.path.abspath(os.path.join(PROJECT_ROOT, script))

    if not os.path.exists(script_path):
        return 1, "", f"Script not found: {script_path}"

    if s['type'] == 'powershell':
        if shutil.which("pwsh"):
            cmd = ["pwsh", "-ExecutionPolicy", "Bypass", "-File", script_path]
        else:
            cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path]
    else:
        cmd = ["/bin/bash", script_path]

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
            "out": out,
            "err": err
        })

    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
