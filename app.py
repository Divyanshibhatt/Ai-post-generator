from openai import OpenAI
import json
import re
import os
import argparse
from datetime import datetime

# -------------------------------
# 🔑 CONFIG
# -------------------------------
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)

PRIMARY_MODEL = "openai/gpt-4o-mini"
FALLBACK_MODEL = "openai/gpt-4o-mini:free"

# -------------------------------
# 🧠 SAFE MODEL CALL
# -------------------------------
def call_model(messages):
    try:
        return client.chat.completions.create(
            model=PRIMARY_MODEL,
            messages=messages,
            temperature=0.6
        )
    except Exception:
        print("⚠️ Primary failed, switching to fallback...")
        return client.chat.completions.create(
            model=FALLBACK_MODEL,
            messages=messages,
            temperature=0.6
        )

# -------------------------------
# 🧹 CLEAN OUTPUT
# -------------------------------
def clean_output(text):
    return text.replace("```json", "").replace("```", "").strip()

def extract_json(text):
    try:
        return json.loads(text)
    except:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError("Invalid JSON")

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'\bn([A-Z#])', r'\n\1', text)
    return text.strip()

# -------------------------------
# 🤖 GENERATION
# -------------------------------
def generate_post(topic, mode):
    prompt = f"""
You are a professional LinkedIn content creator.

TASK:
1. Write a LinkedIn post about: {topic}
2. Tone: {mode}
3. Convert the SAME post into Hinglish

RULES:

ENGLISH:
- Strong hook
- Clean formatting
- Short paragraphs
- 1–2 emojis max
- Add 5–8 hashtags

HINGLISH:
- Natural Hinglish (like Indians speak)
- Same meaning
- No Devanagari
- No weird spacing

OUTPUT STRICT JSON:
{{
  "status": "Approved",
  "compliance_issues": [],
  "content": "string",
  "hinglish": "string"
}}
"""

    response = call_model([{"role": "user", "content": prompt}])
    raw = clean_output(response.choices[0].message.content.strip())

    try:
        result = json.loads(raw)
    except:
        result = extract_json(raw)

    return {
        "status": result.get("status", "Approved"),
        "compliance_issues": result.get("compliance_issues", []),
        "content": clean_text(result.get("content", "")),
        "hinglish": clean_text(result.get("hinglish", "")),
    }

# -------------------------------
# 📦 BATCH GENERATION
# -------------------------------
def generate_batch(topic, mode, count):
    results = []
    for i in range(count):
        print(f"⚡ Generating post {i+1}/{count}...")
        results.append(generate_post(topic, mode))
    return results

# -------------------------------
# 💾 SAVE OUTPUT
# -------------------------------
def save_output(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"linkedin_posts_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Saved to {filename}")

# -------------------------------
# 🖥️ CLI ENTRY
# -------------------------------
def main():
    parser = argparse.ArgumentParser(description="LinkedIn AI Generator")

    parser.add_argument("--topic", type=str, required=True, help="Topic for post")
    parser.add_argument("--mode", type=str, default="professional", help="Tone: viral/professional/casual")
    parser.add_argument("--batch", type=int, default=1, help="Number of posts")

    args = parser.parse_args()

    print("\n🚀 Generating content...\n")

    if args.batch > 1:
        results = generate_batch(args.topic, args.mode, args.batch)
    else:
        results = generate_post(args.topic, args.mode)

    print("\n✅ OUTPUT:\n")
    print(json.dumps(results, indent=2, ensure_ascii=False))

    save_output(results)

# -------------------------------
# RUN
# -------------------------------
if __name__ == "__main__":
    main()