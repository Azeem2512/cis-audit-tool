# Project Scope: CIS Audit Tool

This project implements automated auditing (and optional remediation) for selected CIS Benchmark controls.

We focus on **Level 1** (safe, non-disruptive) controls.

---

## Windows 10/11 Controls
1. win-001: Ensure Windows Defender Antivirus is enabled and running.
2. win-002: Ensure Windows Firewall is enabled on all profiles.
3. win-003: Ensure SMBv1 protocol is disabled.
4. win-004: Ensure Remote Desktop requires Network Level Authentication (NLA).
5. win-005: Ensure password minimum length is set to 14 or more.
6. win-006: Ensure account lockout threshold is configured.
7. win-007: Ensure User Account Control (UAC) is enabled.
8. win-008: Ensure Automatic Updates are enabled.

---

## Linux (Ubuntu 22.04) Controls
1. lin-001: Ensure root login via SSH is disabled.
2. lin-002: Ensure password expiration is 365 days or less.
3. lin-003: Ensure minimum password length is 14 or more.
4. lin-004: Ensure a firewall (ufw or iptables) is active.
5. lin-005: Ensure automatic updates are enabled.
6. lin-006: Ensure auditd service is enabled.
7. lin-007: Ensure /etc/passwd permissions are 644 or more restrictive.
8. lin-008: Ensure /etc/shadow permissions are 640 or more restrictive.
