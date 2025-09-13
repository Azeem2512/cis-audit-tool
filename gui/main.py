import sys, os, platform
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton,
    QVBoxLayout, QWidget, QTextBrowser, QInputDialog, QMessageBox
)
from PySide6.QtCore import QThread, Signal
import subprocess

class AuditRunner(QThread):
    finished = Signal(str)

    def __init__(self, os_choice):
        super().__init__()
        self.os_choice = os_choice

    def run(self):
        # Project root (parent of gui/)
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        orchestrator = os.path.join(base_dir, "backend", "orchestrator.py")
        reports_dir = os.path.join(base_dir, "reports")

        cmd = [sys.executable, orchestrator, self.os_choice]
        proc = subprocess.run(cmd, cwd=base_dir, capture_output=True, text=True)

        report_file = os.path.join(reports_dir, "report.html")

        if os.path.exists(report_file):
            try:
                with open(report_file, "r", encoding="utf-8") as f:
                    html = f.read()
                self.finished.emit(html)
            except Exception as e:
                self.finished.emit(f"<h2>Error reading report</h2><pre>{e}</pre>")
        else:
            self.finished.emit(
                "<h2>No report generated</h2>"
                "<pre>" + proc.stdout + "\n" + proc.stderr + "</pre>"
            )

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CIS Audit Tool")
        self.resize(900, 600)

        self.browser = QTextBrowser()
        self.browser.setOpenExternalLinks(True)

        self.button = QPushButton("Run Audit")
        self.button.clicked.connect(self.run_audit)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def run_audit(self):
        # Detect actual OS
        actual_os = platform.system().lower()   # "windows" or "linux"

        # Ask user for OS choice
        os_choice, ok = QInputDialog.getItem(
            self, "Select OS", "Run audit for:", ["windows", "linux"], 0, False
        )
        if not ok:
            return

        # Validate choice
        if os_choice != actual_os:
            QMessageBox.critical(
                self,
                "OS Mismatch",
                f"You selected '{os_choice}', but this system is actually '{actual_os}'.\n"
                f"Please select the correct OS."
            )
            return

        # Run if valid
        self.button.setEnabled(False)
        self.browser.setHtml(f"<h2>Running {os_choice} audit...</h2>")
        self.thread = AuditRunner(os_choice)
        self.thread.finished.connect(self.display_report)
        self.thread.start()

    def display_report(self, html):
        self.browser.setHtml(html)
        self.button.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
