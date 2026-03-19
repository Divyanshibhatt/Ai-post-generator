
from flask import Flask, request, jsonify
from openai import OpenAI
from localization_agent import translate_to_hindi

app = Flask(__name__)

# Gemini setup
client = OpenAI(
    api_key="AIzaSyChJyrEqhPDv_qqwK_MGsmpZT2XfCApc2w",  
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# -------------------------------
# Compliance Function
# -------------------------------
def check_compliance(content):
    banned_words = ["guarantee", "instant results", "100% sure"]

    issues = []

    for word in banned_words:
        if word in content.lower():
            issues.append(f"Restricted phrase used: {word}")

    if len(content) < 100:
        issues.append("Content too short")

    return issues


# -------------------------------
# Routes
# -------------------------------

@app.route('/')
def home():
    return "Backend is running with Gemini!"

# 🔹 FULL PIPELINE (BEST ROUTE)
@app.route('/process', methods=['POST'])
def process_content():
    data = request.json
    product_info = data.get("product_info", "")

    try:
        # 1. Generate Content
        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {"role": "system", "content": "You are a professional content writer."},
                {"role": "user", "content": f"Write a LinkedIn post about this product:\n{product_info}"}
            ]
        )

        content = response.choices[0].message.content

        # 2. Compliance Check
        issues = check_compliance(content)

        # 3. Translation (Localization)
        hindi_translation = translate_to_hindi(content)

        return jsonify({
            "generated_content": content,
            "compliance_issues": issues,
            "status": "Approved" if not issues else "Needs Review",
            "hindi_translation": hindi_translation
        })

    except Exception as e:
        return jsonify({"error": str(e)})


# -------------------------------
# Run App
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
