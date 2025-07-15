"""
Email.py
Loads sample_emails.json ➜ classifies each email ➜ saves CSV.
"""

import json
import pandas as pd
from classifier import classify_email

INPUT_FILE  = r"C:\Users\tanis\Downloads\sample_emails.json"   # adjust path
OUTPUT_FILE = "classified_emails.csv"

def load_emails(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    emails = load_emails(INPUT_FILE)
    records = []

    for idx, mail in enumerate(emails, start=1):
        print(f"🔎  [{idx}/{len(emails)}] classifying...")
        full_text = f"{mail['subject']}\n{mail['body']}"
        labels = classify_email(full_text)
        records.append({**mail, **labels})

    df = pd.DataFrame(records)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\n✅ All done! Results saved ➜ {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
