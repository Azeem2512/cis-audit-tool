#!/usr/bin/env bash
# check_ufw.sh - Ensure firewall (ufw) is active
if command -v ufw >/dev/null 2>&1; then
  status=$(ufw status | grep -i "Status:" | awk '{print $2}')
  if [ "$status" = "active" ]; then
    echo "PASS: UFW is active"
    exit 0
  else
    echo "FAIL: UFW is not active"
    exit 2
  fi
else
  echo "FAIL: UFW not installed"
  exit 2
fi
