from openai import OpenAI

client = OpenAI(
    api_key="AIzaSyChJyrEqhPDv_qqwK_MGsmpZT2XfCApc2w",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def translate_to_hindi(content):
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content": "You are a professional translator."},
            {"role": "user", "content": f"Translate this into Hindi while keeping tone and meaning:\n{content}"}
        ]
    )

    return response.choices[0].message.content