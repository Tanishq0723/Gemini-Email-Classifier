"""
classifier.py
Gemini email classifier with smart rate‑limit handling
"""

import json
import re
import time
from typing import Dict

import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

# ── 1. Configure ────────────────────────────────────────────────────────────
API_KEY   = "AIzaSyBzMoPbkdENAiBg22VV9H8oYv6JlcZ_g0M"
MODEL_ID  = "models/gemini-2.0-flash"          # fast; use 1.5-pro if you like
MAX_RETRY = 3                                  # retries after 429
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_ID)
# ─────────────────────────────────────────────────────────────────────────────


def _clean_json(raw_text: str) -> Dict:
    """Strip markdown fences and parse JSON."""
    cleaned = re.sub(r"```(?:json)?|```", "", raw_text).strip()
    return json.loads(cleaned)


def classify_email(text: str, attempt: int = 1) -> Dict:
    """
    Call Gemini with back‑off: if a 429 quota error occurs, wait the
    suggested `retry_delay` seconds and retry (up to MAX_RETRY).
    """
    prompt = f"""
You are a business email analyzer.  Respond with valid JSON ONLY:
{{
  "category": "support | complaint | query | spam | other",
  "sentiment": "positive | neutral | negative",
  "urgency":  "high | medium | low"
}}

Email:
\"\"\"{text}\"\"\"
"""

    try:
        response = model.generate_content(prompt)
        return _clean_json(response.text)

    except ResourceExhausted as err:
        if attempt > MAX_RETRY:
            raise RuntimeError("Max retries reached.") from err

        # Gemini includes retry_delay.seconds in the grpc details
        delay = getattr(err, "retry_delay", None)
        wait_s = delay.seconds if delay else 60  # default 60 s
        print(f"⚠️ 429 quota hit. Waiting {wait_s}s then retrying "
              f"(attempt {attempt}/{MAX_RETRY})...")
        time.sleep(wait_s)
        return classify_email(text, attempt + 1)
