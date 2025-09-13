#!/bin/bash
# check_pass_expiry.sh
min_days=$(grep "^PASS_MIN_DAYS" /etc/login.defs | awk '{print $2}')
max_days=$(grep "^PASS_MAX_DAYS" /etc/login.defs | awk '{print $2}')

if [ "$min_days" -ge 1 ] && [ "$max_days" -le 90 ]; then
    echo "PASS: Password expiry policy is configured (min_days=$min_days, max_days=$max_days)"
    exit 0
else
    echo "FAIL: Password expiry policy not properly configured"
    exit 1
fi
