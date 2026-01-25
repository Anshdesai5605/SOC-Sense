# 🛡️ Soc Sense  
### AI-assisted Tier-1 SOC Alert Triage System

Soc Sense is a cybersecurity project designed to reduce SOC alert fatigue.  
It converts noisy and disconnected security alerts into clear, meaningful incidents and uses AI to assist Tier-1 SOC analysts in understanding what happened, how serious it is, and what to check next.

---

## 🚩 Problem Statement
Security Operation Centers (SOCs) receive thousands of alerts every day from different tools.  
Most alerts are isolated, noisy, and difficult to understand. Analysts must manually connect alerts, which leads to alert fatigue, wasted time, and missed real threats.

---

## 💡 Solution
Soc Sense solves this problem by:
- Correlating related security alerts into a single incident using rule-based logic  
- Building a clear, human-readable incident timeline  
- Using AI to act like a Tier-1 SOC analyst and provide:
  - Incident type  
  - Risk level  
  - Confidence score  
  - Recommended next investigation steps  

The system assists human analysts instead of replacing them.

---

## ⚙️ How It Works
1. Raw security alerts are ingested in JSON format  
2. Alerts are correlated using simple rules such as user, IP address, and time window  
3. A step-by-step incident timeline is generated  
4. AI performs Tier-1 SOC triage and produces structured, explainable output  
5. Results are displayed in an interactive Streamlit dashboard  

---

## 🖥️ Tech Stack
- Python  
- Streamlit (Frontend)  
- Google Gemini API (AI reasoning)  
- JSON-based security alerts  

---

## 🚀 Complete Setup & Run Guide

### 1️⃣ Clone the repository
git clone https://github.com/Anshdesai5605/SOC-Sense.git  
cd SOC-Sense  

---

### 2️⃣ Create environment file (IMPORTANT)
Create a file named `.env` in the project root directory and add the line  
GEMINI_API_KEY=your_api_key_here  

Do NOT commit this file. It is already excluded using `.gitignore`.

---

### 3️⃣ Install dependencies
Install the required dependencies using  
pip install -r requirements.txt  

---

### 4️⃣ Run the full application (Backend + Frontend)
Start the application using  
python run_app.py  

The Streamlit UI will open automatically.  
If it does not open, manually go to  
http://localhost:8501  

---

## 📊 Demo Flow
1. View raw security alert noise  
2. See alerts correlated into meaningful incidents  
3. Review AI-generated Tier-1 SOC analysis and recommended next steps  

---

## 🔐 Security
API keys are stored using environment variables.  
The `.env` file is excluded from version control using `.gitignore`.  
No secrets are hardcoded in the source code.

---

## 🎯 Use Case
Soc Sense helps SOC analysts quickly understand real security incidents instead of spending time on isolated and noisy alerts.

---

## 📌 Note
This is a hackathon-ready prototype focused on clarity, explainability, and realistic SOC workflows.
