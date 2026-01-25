import subprocess
import sys

print("Starting AI Tier-1 SOC Analyst UI...")

subprocess.run(
    [sys.executable, "-m", "streamlit", "run", "frontend/app.py"]
)
