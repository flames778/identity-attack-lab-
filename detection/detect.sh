#!/bin/bash
###############################################################################
# Real-time SSH login detection script
#
# Watches /var/log/auth.log and alerts on:
#   - Successful SSH logins (Accepted password / Accepted publickey)
#   - Failed SSH attempts (Failed password)
#   - Invalid user attempts
#
# Usage:
#   chmod +x detect.sh
#   sudo ./detect.sh
###############################################################################

LOG_FILE="/var/log/auth.log"

if [[ ! -r "$LOG_FILE" ]]; then
    echo "❌ Cannot read $LOG_FILE. Run as root."
    exit 1
fi

echo "🔍 Monitoring $LOG_FILE for SSH activity..."
echo "   Press Ctrl+C to stop."
echo "────────────────────────────────────────────"

tail -F "$LOG_FILE" | while read -r line; do
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

    if echo "$line" | grep -q "Accepted password"; then
        USER=$(echo "$line" | awk '{print $9}')
        IP=$(echo "$line" | awk '{print $11}')
        echo "🚨 [$TIMESTAMP] SUCCESSFUL LOGIN — user=$USER src=$IP"
    fi

    if echo "$line" | grep -q "Accepted publickey"; then
        USER=$(echo "$line" | awk '{print $9}')
        IP=$(echo "$line" | awk '{print $11}')
        echo "🚨 [$TIMESTAMP] PUBLICKEY LOGIN — user=$USER src=$IP"
    fi

    if echo "$line" | grep -q "Failed password"; then
        USER=$(echo "$line" | awk '{print $9}')
        IP=$(echo "$line" | awk '{print $11}')
        echo "⚠️  [$TIMESTAMP] FAILED LOGIN — user=$USER src=$IP"
    fi

    if echo "$line" | grep -q "Invalid user"; then
        echo "⚠️  [$TIMESTAMP] INVALID USER — $line"
    fi
done
