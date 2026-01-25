from google import genai
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize Gemini client securely
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """
You are a Tier-1 SOC analyst.

Your task:
Analyze the given security incident timeline and return a structured assessment.

STRICT RULES:
- You MUST return ONLY valid JSON
- Do NOT include explanations, markdown, or text outside JSON
- Do NOT invent facts not present in the timeline

OUTPUT FORMAT (EXACT):
{
  "incident_type": "string",
  "risk_level": "low | medium | high",
  "confidence": number between 0 and 1,
  "evidence_summary": "string",
  "recommended_next_steps": ["string", "string"]
}
"""

def analyze_incident(timeline):
    prompt = SYSTEM_PROMPT + "\n\nIncident Timeline:\n" + "\n".join(timeline)

    response = client.models.generate_content(
        model="models/gemini-flash-lite-latest",
        contents=prompt
    )

    raw_text = response.text.strip()

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        return {
            "incident_type": "unknown",
            "risk_level": "medium",
            "confidence": 0.5,
            "evidence_summary": "AI response could not be parsed as valid JSON.",
            "recommended_next_steps": [
                "Manually review the correlated alerts",
                "Validate alert sources"
            ],
            "raw_ai_output": raw_text
        }
