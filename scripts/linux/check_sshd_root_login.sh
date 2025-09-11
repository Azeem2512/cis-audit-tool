#!/usr/bin/env bash
CONF="/etc/ssh/sshd_config"
if grep -Eiq '^\s*PermitRootLogin\s+no' "$CONF"; then
  echo "PASS: PermitRootLogin is disabled"
  exit 0
else
  echo "FAIL: PermitRootLogin not explicitly set to no"
  exit 2
fi
