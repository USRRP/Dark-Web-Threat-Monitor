
from config import keywords

def scan_for_alerts(text):
    alerts = []
    for line in text.splitlines():
        for word in keywords:
            if word.lower() in line.lower():
                alerts.append((word, line.strip()))
    return alerts
