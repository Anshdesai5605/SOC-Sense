import streamlit as st
import subprocess
import json
import os
import sys

st.set_page_config(
    page_title="SocSense | Tier-1 AI Analyst",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
def local_css():
    st.markdown("""
    <style>
        /* Hide Streamlit default header (Deploy button, hamburger menu) */
        [data-testid="stHeader"] {
            display: none !important;
        }
        #MainMenu {
            visibility: hidden;
        }
        footer {
            visibility: hidden;
        }

        /* Modern SIEM Background - Sleek Dark Gradient */
        .stApp {
            background-color: #050505 !important;
            background-image: 
                radial-gradient(circle at 50% 0%, rgba(0, 255, 0, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 100% 100%, rgba(0, 70, 255, 0.05) 0%, transparent 50%);
            background-attachment: fixed;
        }

        /* General layout: minimal padding */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 0.5rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
            max-width: 95% !important;
            position: relative;
            z-index: 10;
        }
        /* Headers: much smaller and modern */
        h1 {
            font-size: 1.8rem !important;
            font-weight: 700 !important;
            margin-bottom: 0px !important;
            padding-bottom: 0px !important;
            color: #45f3ff !important;
            text-shadow: 0 0 10px rgba(69, 243, 255, 0.5);
            letter-spacing: 2px;
        }
        h2 {
            font-size: 1.2rem !important;
            font-weight: 500 !important;
            margin-top: 0.5rem !important;
            margin-bottom: 0px !important;
            padding-bottom: 0px !important;
            color: #00ff00 !important;
            text-shadow: 0 0 5px rgba(0, 255, 0, 0.4);
            text-transform: uppercase;
        }
        h3 {
            font-size: 0.95rem !important;
            margin-bottom: 0.2rem !important;
            color: #a0a0a0 !important;
            text-transform: uppercase;
            letter-spacing: 1px;
            border-bottom: 1px solid rgba(0, 255, 0, 0.2);
            padding-bottom: 4px;
        }
        /* Paragraphs and normal text */
        p, div, span, label {
            font-size: 0.85rem !important;
            line-height: 1.4 !important;
            margin-bottom: 0.2rem !important;
            color: #c5c6c7;
        }
        /* Code blocks / JSON */
        pre {
            font-size: 0.7rem !important;
            line-height: 1.3 !important;
            padding: 0.8rem !important;
            background-color: rgba(0, 0, 0, 0.6) !important;
            border-left: 3px solid #00ff00 !important;
            border-radius: 4px;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.8);
        }
        /* Expander headers */
        .streamlit-expanderHeader {
            font-size: 0.85rem !important;
            color: #45f3ff !important;
            padding: 0.4rem 0.5rem !important;
            min-height: 2rem !important;
            background: rgba(0, 255, 0, 0.05);
            border: 1px solid rgba(0, 255, 0, 0.2);
            border-radius: 4px;
            transition: 0.3s;
        }
        .streamlit-expanderHeader:hover {
            background: rgba(0, 255, 0, 0.15);
            box-shadow: 0 0 10px rgba(0, 255, 0, 0.2);
        }
        
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(0, 255, 0, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(0, 255, 0, 0); }
            100% { box-shadow: 0 0 0 0 rgba(0, 255, 0, 0); }
        }

        /* Buttons: sleek outline */
        .stButton>button {
            width: 100%;
            border: 1px solid #00ff00 !important;
            color: #00ff00 !important;
            background-color: rgba(0, 255, 0, 0.05) !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            padding: 0.4rem !important;
            min-height: 2.5rem !important;
            border-radius: 4px;
            transition: all 0.3s ease-in-out;
            text-transform: uppercase;
            letter-spacing: 1px;
            position: relative;
            overflow: hidden;
        }
        .stButton>button::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 300%;
            height: 300%;
            background: rgba(0, 255, 0, 0.1);
            transition: all 0.5s ease;
            transform: translate(-50%, -50%) rotate(45deg);
            opacity: 0;
        }
        .stButton>button:hover::before {
            opacity: 1;
        }
        .stButton>button:hover {
            background-color: rgba(0, 255, 0, 0.2) !important;
            color: #fff !important;
            box-shadow: 0 0 15px rgba(0,255,0,0.5);
            animation: pulse 1.5s infinite;
        }
        /* Container borders - Glassmorphism */
        .stContainer > div {
            border: 1px solid rgba(69, 243, 255, 0.2) !important;
            border-radius: 8px !important;
            padding: 1rem !important;
            background: rgba(10, 15, 20, 0.7) !important;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(5px);
            -webkit-backdrop-filter: blur(5px);
            transition: 0.3s ease;
        }
        .stContainer > div:hover {
            border-color: rgba(69, 243, 255, 0.6) !important;
            box-shadow: 0 0 20px rgba(69, 243, 255, 0.15);
            transform: translateY(-2px);
        }
        
        /* Metric Styling */
        [data-testid="stMetricValue"] {
            font-size: 2rem !important;
            color: #00ff00 !important;
            text-shadow: 0 0 10px rgba(0, 255, 0, 0.3);
            font-family: 'Courier New', Courier, monospace;
        }
        [data-testid="stMetricLabel"] {
            color: #45f3ff !important;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-size: 0.9rem !important;
        }

        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px;
            background-color: rgba(0,0,0,0.3);
            padding: 5px 5px 0 5px;
            border-radius: 8px 8px 0 0;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 0.6rem 1.2rem !important;
            border-radius: 6px 6px 0px 0px;
            background-color: rgba(30, 30, 30, 0.6);
            color: #888;
            border: 1px solid transparent;
            border-bottom: none;
            transition: 0.3s;
        }
        .stTabs [data-baseweb="tab"]:hover {
            color: #fff;
            background-color: rgba(50, 50, 50, 0.8);
        }
        .stTabs [aria-selected="true"] {
            background-color: rgba(0, 255, 0, 0.1) !important;
            color: #00ff00 !important;
            border: 1px solid rgba(0, 255, 0, 0.3) !important;
            border-bottom: none !important;
            box-shadow: inset 0 2px 5px rgba(0, 255, 0, 0.2);
            font-weight: bold;
        }
        
        /* Download Button Styling */
        [data-testid="stDownloadButton"] > button {
            width: 100%;
            border: 1px dashed #00ff00 !important;
            color: #00ff00 !important;
            background-color: rgba(0, 255, 0, 0.05) !important;
            font-weight: 500 !important;
            font-size: 0.8rem !important;
            margin-top: 1rem;
        }
        [data-testid="stDownloadButton"] > button:hover {
            background-color: rgba(0, 255, 0, 0.2) !important;
            box-shadow: 0 0 10px rgba(0, 255, 0, 0.4);
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #050505 !important;
            border-right: 1px solid rgba(0, 255, 0, 0.2) !important;
        }
        [data-testid="stSidebar"] h1 {
            color: #00ff00 !important;
            text-shadow: 0 0 8px rgba(0,255,0,0.5);
            font-size: 1.4rem !important;
        }
        
        /* Divider */
        hr {
            margin: 1rem 0 !important;
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(0, 255, 0, 0.5), transparent) !important;
        }
        
        /* Animations on elements */
        .element-container {
            animation: fadeIn 0.5s ease-in-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
    """, unsafe_allow_html=True)

local_css()

def generate_report_markdown(inc):
    """Generates a clean Markdown report from an incident dictionary."""
    analysis = inc.get('ai_analysis', {})
    
    md_report = f"# SocSense Incident Report: {inc['incident_id']}\n\n"
    
    md_report += "## Executive Summary\n"
    md_report += f"- **Classification:** {analysis.get('incident_type', 'Unknown')}\n"
    md_report += f"- **Risk Severity:** {analysis.get('risk_level', 'Unknown').upper()}\n"
    
    conf = analysis.get('confidence', 'N/A')
    conf_display = f"{int(conf * 100)}%" if isinstance(conf, (int, float)) else str(conf)
    md_report += f"- **Analyst Confidence:** {conf_display}\n\n"
    
    md_report += "## Timeline\n"
    for event in inc.get('timeline', []):
        md_report += f"- {event}\n"
        
    md_report += "\n## AI Assessment & Evidence\n"
    md_report += f"{analysis.get('evidence_summary', 'No summary provided.')}\n\n"
    
    md_report += "## Recommended Next Steps\n"
    for step in analysis.get('recommended_next_steps', []):
        md_report += f"- {step}\n"
        
    md_report += "\n---\n*Report generated by SocSense AI Tier-1 Analyst*"
    return md_report

# Resolve paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "backend", "main.py"))
UPLOAD_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "uploads"))

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

# -----------------------------
# SIDEBAR CONTROL PANEL
# -----------------------------
with st.sidebar:
    st.title("🛡️ SocSense Control Center")
    st.caption("Data Ingestion & Correlation")
    
    st.divider()
    
    st.markdown("### Telemetry Ingestion")
    uploaded_file = st.file_uploader("Upload Event Logs (JSON)", type=["json"], label_visibility="collapsed")
    
    data_path = None
    raw_alerts = []
    
    if uploaded_file is not None:
        try:
            raw_alerts = json.load(uploaded_file)
            data_path = os.path.join(UPLOAD_DIR, "temp_upload.json")
            with open(data_path, "w") as f:
                json.dump(raw_alerts, f)
            st.success(f"{len(raw_alerts)} events staged.", icon="✅")
        except json.JSONDecodeError:
            st.error("Invalid JSON file uploaded.")
    
    st.divider()
    
    st.markdown("### Threat Engine")
    run_pressed = st.button("▶ INITIALIZE CORRELATION ENGINE", disabled=uploaded_file is None)

# -----------------------------
# MAIN DASHBOARD HEADER
# -----------------------------
st.title("SocSense")
st.caption("Automated Threat Correlation & AI-Driven Incident Triage Dashboard")
st.divider()

# -----------------------------
# LOGIC & EXECUTION
# -----------------------------
if not data_path and not run_pressed:
    # Empty State
    st.info("System Ready: Awaiting telemetry ingestion from Control Center. Please upload a structured JSON event log to begin.")
    
    # Show metric placeholders
    col1, col2, col3 = st.columns(3)
    col1.metric("Telemetry Ingested", "0 Events")
    col2.metric("Correlated Incidents", "0")
    col3.metric("System Status", "Standby")

elif run_pressed and data_path:
    with st.spinner("Executing correlation rules and initializing AI Analyst assessment..."):
        try:
            result = subprocess.run(
                [sys.executable, BACKEND_PATH, data_path],
                capture_output=True,
                text=True,
                check=True
            )
            incidents = json.loads(result.stdout)
            
            # Show active metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Telemetry Ingested", f"{len(raw_alerts)} Events")
            col2.metric("Correlated Incidents", len(incidents))
            col3.metric("System Status", "Processing Complete", delta="Active", delta_color="normal")
            
            st.divider()
            
            # -----------------------------
            # INCIDENT VIEWER (TABS)
            # -----------------------------
            if incidents:
                tab_names = [f"🚨 {inc['incident_id']}" for inc in incidents]
                tabs = st.tabs(tab_names)
                
                for idx, tab in enumerate(tabs):
                    with tab:
                        inc = incidents[idx]
                        st.subheader(f"Incident Analysis: {inc['incident_id']}")
                        
                        # Two column inner layout
                        col_timeline, col_ai = st.columns([1, 1.5])
                        
                        with col_timeline:
                            with st.container():
                                st.markdown("### 📅 Execution Timeline")
                                st.caption("Chronological reconstruction of correlated security events.")
                                for event in inc["timeline"]:
                                    st.info(event)
                                
                                with st.expander("▶ INSPECT RAW EVENT LOG PAYLOAD", expanded=False):
                                    st.code(json.dumps(raw_alerts, indent=2), language="json")
                                
                        with col_ai:
                            with st.container():
                                st.markdown("### 🤖 AI Assessment")
                                st.caption("Automated SOC Analyst reasoning and recommended remediation.")
                                
                                analysis = inc.get("ai_analysis", {})
                                
                                # Render fields cleanly
                                st.markdown(f"**Classification:** `{analysis.get('incident_type', 'Unknown')}`")
                                
                                risk = analysis.get('risk_level', 'Unknown')
                                color = "red" if risk.lower() == "critical" or risk.lower() == "high" else "orange" if risk.lower() == "medium" else "green"
                                st.markdown(f"**Risk Severity:** :{color}[**{risk.upper()}**]")
                                
                                conf = analysis.get('confidence', 'N/A')
                                if isinstance(conf, (int, float)):
                                    conf_display = f"{int(conf * 100)}%"
                                else:
                                    conf_display = str(conf)
                                st.markdown(f"**Analyst Confidence:** {conf_display}")
                                
                                st.markdown("---")
                                st.markdown("**Evidence Summary:**")
                                st.write(analysis.get('evidence_summary', 'No summary provided.'))
                                
                                st.markdown("**Recommended Next Steps:**")
                                next_steps = analysis.get('recommended_next_steps', [])
                                if next_steps:
                                    for step in next_steps:
                                        st.markdown(f"- {step}")
                                else:
                                    st.write("No steps provided.")
                                    
                                st.download_button(
                                    label="📥 Download Threat Report (MD)",
                                    data=generate_report_markdown(inc),
                                    file_name=f"SocSense_Report_{inc['incident_id']}.md",
                                    mime="text/markdown"
                                )

            else:
                st.success("Analysis complete. Zero threat incidents detected from the ingested telemetry.")
                
        except subprocess.CalledProcessError as e:
            st.error("Correlation Engine Execution Failed.")
            st.code(e.stderr)

        except json.JSONDecodeError:
            st.error("Failed to parse backend output stream.")
            st.code(result.stdout)

st.markdown("---")
st.caption("SocSense SIEM v1.0.0 | Enterprise Edition")
