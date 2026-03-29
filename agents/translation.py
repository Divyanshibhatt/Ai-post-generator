from utils import call_model

def translation_agent(text):
    """
    Convert English post to Hinglish
    """
    prompt = f"Convert this into Hinglish:\n{text}"
    res = call_model([{"role": "user", "content": prompt}])
    return res.choices[0].message.content.strip()
