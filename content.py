from utils import call_model, clean_output, extract_json

def planner_agent(topic, mode):
    prompt = f"""
Plan a LinkedIn post on: {topic}
Tone: {mode}

Return JSON:
{{
  "hook": "...",
  "points": ["...", "..."]
}}
"""
    res = call_model([{"role": "user", "content": prompt}])
    return extract_json(clean_output(res.choices[0].message.content))