from utils import call_model

def moderator_agent(text):
    prompt = f"""
Improve this LinkedIn post if needed:

{text}
"""
    res = call_model([{"role": "user", "content": prompt}])
    return res.choices[0].message.content.strip()
