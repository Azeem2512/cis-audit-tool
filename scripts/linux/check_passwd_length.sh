#!/usr/bin/env bash
# check_passwd_length.sh - Ensure minimum password length is 14 or more
CONF="/etc/login.defs"
minlen=$(grep -Ei '^\s*PASS_MIN_LEN' "$CONF" | awk '{print $2}')

if [ -z "$minlen" ]; then
  echo "FAIL: PASS_MIN_LEN not set"
  exit 2
elif [ "$minlen" -ge 14 ]; then
  echo "PASS: PASS_MIN_LEN is $minlen"
  exit 0
else
  echo "FAIL: PASS_MIN_LEN is $minlen (less than 14)"
  exit 2
fi
