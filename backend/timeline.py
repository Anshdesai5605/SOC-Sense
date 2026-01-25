def build_timeline(alerts):
    sorted_alerts = sorted(alerts, key=lambda x: x["timestamp"])
    timeline = []

    for alert in sorted_alerts:
        timeline.append(
            f'{alert["timestamp"]} – {alert["event_type"]} on {alert["resource"]}'
        )

    return timeline
