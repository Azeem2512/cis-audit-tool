#!/bin/bash
# check_firewall.sh
if command -v ufw >/dev/null 2>&1; then
    status=$(ufw status | grep -i "Status: active")
    if [ -n "$status" ]; then
        echo "PASS: UFW firewall enabled"
        exit 0
    else
        echo "FAIL: UFW firewall not enabled"
        exit 1
    fi
elif command -v iptables >/dev/null 2>&1; then
    rules=$(iptables -L)
    if [ -n "$rules" ]; then
        echo "PASS: iptables rules are configured"
        exit 0
    else
        echo "FAIL: iptables has no rules"
        exit 1
    fi
else
    echo "FAIL: No firewall tool found (UFW/iptables)"
    exit 1
fi
