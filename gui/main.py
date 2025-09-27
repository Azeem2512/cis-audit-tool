# gui/main.py
import sys
import subprocess
import json
import os
import datetime
import re
import platform
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QRadioButton, QGroupBox
)
from PySide6.QtCore import Qt

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend import orchestrator

# --- Logging setup ---
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

def log_error(message: str) -> str:
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(LOG_DIR, f"errors_{timestamp}.log")
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(message)
    return log_file

# --- Audit functions ---
def run_audit(selected_os):
    cmd = [sys.executable, "-m", "backend.orchestrator", selected_os]
    proc = subprocess.run(cmd, capture_output=True, text=True)

    try:
        # Use regex to extract the first JSON array from stdout
        match = re.search(r'(\[\s*{.*?}\s*\])', proc.stdout, re.DOTALL)
        if not match:
            raise ValueError("No JSON array found in orchestrator output")
        json_text = match.group(1)
        results = json.loads(json_text)
    except Exception:
        import traceback
        log_file = log_error(traceback.format_exc() + "\nOutput:\n" + proc.stdout)
        QMessageBox.critical(
            None,
            "Error",
            f"Failed to parse results.\nFull error saved to:\n{log_file}"
        )
        return []

    return results


def fix_issue(test_id, fix_description, selected_os, table):
    confirm = QMessageBox.question(
        None,
        "Confirm Fix",
        f"This will apply:\n\n{fix_description}\n\nDo you want to continue?",
        QMessageBox.Yes | QMessageBox.No
    )
    if confirm != QMessageBox.Yes:
        return

    try:
        result = orchestrator.run_fix(test_id)
        if "error" in result:
            QMessageBox.critical(None, "Fix Error", result["error"])
        else:
            QMessageBox.information(None, "Fix Result", f"{result['title']}\n\n{result['out']}")
    except Exception:
        import traceback
        log_file = log_error(traceback.format_exc())
        QMessageBox.critical(
            None,
            "Fix Error",
            f"An error occurred while applying the fix.\nFull error saved to:\n{log_file}"
        )

    refreshed = run_audit(selected_os)
    update_table(table, refreshed, selected_os)

def update_table(table, results, selected_os):
    table.setRowCount(0)
    for r in results:
        if r.get("os") != selected_os:
            continue  # Only show results for the selected OS

        if "Skipped" in r.get("out", ""):
            continue  # Don't show skipped checks for other OS

        if r["rc"] == 0:
            status = "PASS"
        elif r["rc"] != 0:
            status = "FAIL"
        else:
            status = "ERROR"

        row = table.rowCount()
        table.insertRow(row)
        table.setItem(row, 0, QTableWidgetItem(r["id"]))
        table.setItem(row, 1, QTableWidgetItem(r["title"]))
        table.setItem(row, 2, QTableWidgetItem(status))
        table.setItem(row, 3, QTableWidgetItem(r["out"]))

        if r.get("has_fix") and status in ("FAIL", "SKIP"):
            btn = QPushButton("Fix")
            btn.clicked.connect(lambda _, rid=r["id"], desc=r["fix_description"]: fix_issue(rid, desc, selected_os, table))
            table.setCellWidget(row, 4, btn)

USER_OS = platform.system().lower()  # "windows" or "linux"

# --- GUI ---
class AuditApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CIS Audit Tool")
        layout = QVBoxLayout()

        # OS selector
        self.os_group = QGroupBox("Select OS")
        os_layout = QHBoxLayout()
        self.radio_win = QRadioButton("Windows")
        self.radio_linux = QRadioButton("Linux")
        # Default to user's OS
        if USER_OS == "windows":
            self.radio_win.setChecked(True)
        else:
            self.radio_linux.setChecked(True)
        os_layout.addWidget(self.radio_win)
        os_layout.addWidget(self.radio_linux)
        self.os_group.setLayout(os_layout)
        layout.addWidget(self.os_group)

        # Run Audit button
        self.run_btn = QPushButton("Run Audit")
        self.run_btn.clicked.connect(self.run_audit_clicked)
        layout.addWidget(self.run_btn)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Title", "Status", "Output", "Fix"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def run_audit_clicked(self):
        selected_os = "windows" if self.radio_win.isChecked() else "linux"
        if selected_os != USER_OS:
            QMessageBox.critical(
                self,
                "OS Mismatch",
                f"You are running this tool on {USER_OS.capitalize()}, but selected {selected_os.capitalize()}.\n"
                "Please select the correct OS."
            )
            return
        results = run_audit(selected_os)
        update_table(self.table, results, selected_os)

# --- Run application ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AuditApp()
    window.resize(900, 500)
    window.show()
    sys.exit(app.exec())
