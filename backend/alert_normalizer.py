def normalize_alert(alert):
    return {
        "alert_id": alert.get("alert_id"),
        "timestamp": alert.get("timestamp"),
        "source": alert.get("source", "unknown"),
        "event_type": alert.get("event_type"),
        "severity": alert.get("severity", "low"),
        "user": alert.get("user", "unknown"),
        "ip_address": alert.get("ip_address", "unknown"),
        "location": alert.get("location", "unknown"),
        "resource": alert.get("resource", "unknown")
    }
