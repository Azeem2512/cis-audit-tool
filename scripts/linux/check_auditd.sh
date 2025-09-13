#!/usr/bin/env bash
# check_auditd.sh - Ensure auditd service is running
if systemctl is-active --quiet auditd; then
  echo "PASS: auditd service is running"
  exit 0
else
  echo "FAIL: auditd service is not running"
  exit 2
fi
