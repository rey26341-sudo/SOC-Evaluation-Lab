import json
from collections import Counter
from datetime import datetime

THRESHOLD_MEDIUM = 5
THRESHOLD_HIGH = 10

with open("logs/auth_logs.json", "r") as f:
    logs = json.load(f)

failed_ips = []

for event in logs:

    if event["event_type"] == "failed_login":
        failed_ips.append(event["source_ip"])

ip_counts = Counter(failed_ips)

alerts = []

for ip, count in ip_counts.items():

    severity = None

    if count >= THRESHOLD_HIGH:
        severity = "HIGH"

    elif count >= THRESHOLD_MEDIUM:
        severity = "MEDIUM"

    if severity:

        alert = {
            "timestamp": datetime.utcnow().isoformat(),
            "source_ip": ip,
            "failed_attempts": count,
            "severity": severity,
            "alert_type": "Brute Force Detected"
        }

        alerts.append(alert)

print("\n=== ALERTS ===\n")

for alert in alerts:
    print(alert)

with open("logs/alerts.json", "w") as f:
    json.dump(alerts, f, indent=4)

print("\n[+] Alerts saved to logs/alerts.json")