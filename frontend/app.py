import streamlit as st
import subprocess
import json
import os
import sys

st.set_page_config(
    page_title="AI Tier-1 SOC Analyst",
    layout="wide"
)

st.title("🛡️ AI Tier-1 SOC Analyst")
st.subheader("Reducing SOC alert fatigue using correlation + AI reasoning")

st.write(
    """
This demo shows how **raw, noisy security alerts** are transformed into
**clear, actionable incidents** using rule-based correlation and AI-assisted Tier-1 triage.
"""
)

# Resolve paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "backend", "main.py"))
DATA_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "sample_alerts.json"))

st.divider()

# -----------------------------
# SECTION 1: RAW ALERTS
# -----------------------------
st.header("🔴 Step 1: Raw Security Alerts (Alert Noise)")

st.write(
    "These are the raw alerts a SOC analyst receives from cloud and identity systems. "
    "Individually, they lack context and are difficult to triage."
)

with open(DATA_PATH) as f:
    raw_alerts = json.load(f)

st.code(json.dumps(raw_alerts, indent=2), language="json")

st.divider()

# -----------------------------
# SECTION 2: RUN ANALYSIS
# -----------------------------
st.header("🟡 Step 2: Correlate Alerts & Build Incidents")

st.write(
    "Alerts are correlated using deterministic rules (user, IP, time window) "
    "to form meaningful incident candidates."
)

if st.button("▶ Run SOC Analysis"):
    st.info("Running backend correlation and AI analysis...")

    try:
        result = subprocess.run(
            [sys.executable, BACKEND_PATH],
            capture_output=True,
            text=True,
            check=True
        )

        incidents = json.loads(result.stdout)

        st.success("Correlation completed. Incidents identified.")

        st.divider()

        # -----------------------------
        # SECTION 3: INCIDENT VIEW
        # -----------------------------
        st.header("🟢 Step 3: AI Tier-1 SOC Triage")

        for inc in incidents:
            st.subheader(f"🚨 Incident {inc['incident_id']}")

            col1, col2 = st.columns([1, 1])

            with col1:
                st.markdown("### 📅 Incident Timeline")
                st.write(
                    "This timeline reconstructs the sequence of related alerts "
                    "into a single security narrative."
                )
                for event in inc["timeline"]:
                    st.write(f"- {event}")

            with col2:
                st.markdown("### 🤖 AI Tier-1 Assessment")
                st.write(
                    "Gemini analyzes the incident like a Tier-1 SOC analyst, "
                    "assessing risk and recommending next steps."
                )
                st.json(inc["ai_analysis"])

            st.divider()

    except subprocess.CalledProcessError as e:
        st.error("Backend execution failed.")
        st.code(e.stderr)

    except json.JSONDecodeError:
        st.error("Failed to parse backend output.")
        st.code(result.stdout)

st.caption(
    "Hackathon Demo | AI-assisted Tier-1 SOC triage | Rule-based correlation + explainable AI"
)
