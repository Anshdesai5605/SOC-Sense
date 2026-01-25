import json
import os

from alert_normalizer import normalize_alert
from correlator import correlate_alerts
from timeline import build_timeline
from ai_analyzer import analyze_incident

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "sample_alerts.json")

with open(DATA_PATH) as f:
    raw_alerts = json.load(f)

alerts = [normalize_alert(a) for a in raw_alerts]
incidents = correlate_alerts(alerts)

results = []

for idx, incident in enumerate(incidents):
    timeline = build_timeline(incident)
    ai_result = analyze_incident(timeline)

    results.append({
        "incident_id": f"INC-{idx+1}",
        "timeline": timeline,
        "ai_analysis": ai_result
    })

print(json.dumps(results, indent=2))
