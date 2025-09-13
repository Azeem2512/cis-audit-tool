#!/bin/bash
# check_unattended_upgrades.sh
if dpkg -l | grep -q unattended-upgrades; then
    status=$(systemctl is-enabled unattended-upgrades 2>/dev/null)
    if [ "$status" = "enabled" ]; then
        echo "PASS: Unattended-upgrades enabled"
        exit 0
    else
        echo "FAIL: Unattended-upgrades not enabled"
        exit 1
    fi
else
    echo "FAIL: Unattended-upgrades not installed"
    exit 1
fi
