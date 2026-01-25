from datetime import datetime, timedelta

TIME_WINDOW_MINUTES = 30

def correlate_alerts(alerts):
    incidents = []
    used = set()

    for i, alert in enumerate(alerts):
        if i in used:
            continue

        incident = [alert]
        used.add(i)

        for j, other in enumerate(alerts):
            if j in used:
                continue

            same_user = alert["user"] == other["user"]
            same_ip = alert["ip_address"] == other["ip_address"]

            t1 = datetime.fromisoformat(alert["timestamp"].replace("Z", ""))
            t2 = datetime.fromisoformat(other["timestamp"].replace("Z", ""))

            if same_user and same_ip and abs(t1 - t2) <= timedelta(minutes=TIME_WINDOW_MINUTES):
                incident.append(other)
                used.add(j)

        incidents.append(incident)

    return incidents
