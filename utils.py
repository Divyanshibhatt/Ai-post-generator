import json, re, os
from openai import OpenAI
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("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")
)
def call_model(messages):
    return client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=messages
    )
def clean_output(text):
    return text.replace("```json", "").replace("```", "").strip()
def extract_json(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    return json.loads(match.group())
