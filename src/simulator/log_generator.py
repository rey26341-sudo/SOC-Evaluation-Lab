import json
import random
from datetime import datetime

users = ["admin", "john", "finance", "guest"]

ips = [
    "185.220.101.1",
    "45.33.32.156",
    "103.77.192.44",
    "192.168.1.10"
]

events = []

for _ in range(50):

    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": "failed_login",
        "username": random.choice(users),
        "source_ip": random.choice(ips),
        "status": "failed"
    }

    events.append(event)

with open("logs/auth_logs.json", "w") as f:
    json.dump(events, f, indent=4)

print("[+] Security logs generated.")