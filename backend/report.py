import json, datetime, os

def generate_html_report(results, reports_dir="reports"):
    # Ensure reports directory exists
    os.makedirs(reports_dir, exist_ok=True)

    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(reports_dir, f"report_{timestamp}.html")

    rows = ""
    for r in results:
        # Skip entries that were skipped due to OS mismatch
        if r.get("out") == r.get("err") and "Skipped" in r.get("out", ""):
            continue

        status = "PASS" if r["rc"] == 0 else "FAIL" if r["rc"] == 2 else "SKIP/ERROR"
        color = "green" if status == "PASS" else "red" if status == "FAIL" else "gray"
        rows += f"""
        <tr>
            <td>{r['id']}</td>
            <td>{r['title']}</td>
            <td style="color:{color}; font-weight:bold;">{status}</td>
            <td><pre>{r['out']}</pre></td>
        </tr>
        """

    html = f"""
    <html>
    <head>
        <title>CIS Audit Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #333; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ccc; padding: 8px; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>CIS Audit Report</h1>
        <p>Generated: {now.strftime("%Y-%m-%d %H:%M:%S")}</p>
        <table>
            <tr><th>ID</th><th>Title</th><th>Status</th><th>Output</th></tr>
            {rows}
        </table>
    </body>
    </html>
    """
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[+] Report generated: {output_file}")
