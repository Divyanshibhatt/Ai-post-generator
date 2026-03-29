import streamlit as st
from app import generate_batch

# -------------------------------
# ⚙️ PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="AI Content System",
    page_icon="🚀",
    layout="wide"
)

# -------------------------------
# 🎨 CSS
# -------------------------------
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background: #ffffff !important;  /* white background */
}
textarea, input {
    background: #f9f9f9 !important;
    color: #111827 !important;
    border-radius: 10px !important;
    padding: 10px !important;
}
.result-card {
    background: #ffffff !important;
    color: #111827 !important;
    padding: 20px;
    border-radius: 14px;
    margin-top: 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #38bdf8, #6366f1);
    color: white !important;
    border-radius: 10px;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# 🖥️ HEADER
# -------------------------------
st.title("🚀 AI Content Lifecycle System")
st.markdown("Multi-Agent AI for LinkedIn Content Generation")
st.markdown("---")

# -------------------------------
# 🧾 INPUTS
# -------------------------------
topic = st.text_area(
    "📌 Enter Topic",
    placeholder="e.g. Future of AI in India",
    key="topic"
)

col1, col2 = st.columns(2)

with col1:
    mode = st.selectbox(
        "🎯 Tone",
        ["professional", "casual", "motivational"],
        key="mode"
    )

with col2:
    lang = st.selectbox(
        "🌐 Language",
        ["both", "english", "hinglish"],
        key="lang"
    )

batch = st.number_input(
    "📦 Number of Posts",
    min_value=1,
    max_value=10,
    value=1,
    key="batch"
)

length = st.selectbox(
    "📝 Post Length",
    ["short", "medium", "long"],
    key="length"
)

generate_btn = st.button("✨ Generate Content")

# -------------------------------
# 🚀 OUTPUT
# -------------------------------
if generate_btn:
    if topic.strip() == "":
        st.warning("⚠️ Please enter a topic")
    else:
        with st.spinner("🤖 Agents are working..."):
            results = generate_batch(topic, mode, lang, batch, length)

        st.success("✅ Generated with Multi-Agent AI System")

        all_text = ""

        for i, r in enumerate(results):
            st.markdown('<div class="result-card">', unsafe_allow_html=True)

            st.markdown(f"### 📄 Post {i+1}")
            st.markdown(f"**Status:** {r.get('status', 'Approved')}")

            # English
            if "content" in r:
                with st.expander("📌 English"):
                    st.text_area(
                        "English Content",
                        value=r["content"],
                        height=200,
                        key=f"eng_{i}",
                        label_visibility="collapsed"
                    )
                    all_text += f"Post {i+1} (English)\n{r['content']}\n\n"

            # Hinglish
            if "hinglish" in r:
                with st.expander("📌 Hinglish"):
                    st.text_area(
                        "Hinglish Content",
                        value=r["hinglish"],
                        height=200,
                        key=f"hing_{i}",
                        label_visibility="collapsed"
                    )
                    all_text += f"Post {i+1} (Hinglish)\n{r['hinglish']}\n\n"

            st.markdown('</div>', unsafe_allow_html=True)

        st.download_button(
            "⬇️ Download All Posts",
            all_text,
            file_name="linkedin_posts.txt"
        )

# -------------------------------
# 💡 FOOTER
# -------------------------------
st.markdown("---")
st.info("💡 Tip: Copy and post directly on LinkedIn for best engagement 🚀")
