import streamlit as st
from app import generate_post
st.set_page_config(
    page_title="AI Content System",
    page_icon="🚀",
    layout="wide"
)
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(-45deg, #334155, #475569, #1e293b, #60a5fa);
    background-size: 400% 400%;
    animation: gradientMove 12s ease infinite;
}
@keyframes gradientMove {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
textarea, input {
    background: rgba(255,255,255,0.95) !important;
    color: #111827 !important;
    border-radius: 10px !important;
}
.result-card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    margin-top: 20px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}
.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #38bdf8, #6366f1);
    color: white;
    border-radius: 10px;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)
st.title("🚀 AI Content Lifecycle System")
st.markdown("Multi-Agent AI for LinkedIn Content Generation")
st.markdown("---")
topic = st.text_area(
    "📌 Enter Topic",
    placeholder="e.g. Future of AI in India",
    key="topic"
)
col1, col2=st.columns(2)
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
    ["short","medium","long"],
    key="length"
)
generate_btn = st.button("✨ Generate Content")
if generate_btn:
    if topic.strip()=="":
        st.warning("⚠️ Please enter a topic")
    else:
        with st.spinner("🤖 Agents are working..."):
            results =[]
            for _ in range(batch):
                results.append(generate_post(topic, mode, lang, length))
        st.success("✅ Content Generated Successfully!")
        all_text = ""
        for i, r in enumerate(results):
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown(f"### 📄 Post {i+1}")
            st.markdown(f"**Status:** {r.get('status', 'Approved')}")
            if "content" in r:
                with st.expander("📌English"):
                    st.write(r["content"])
                    all_text += f"Post {i+1} (English)\n{r['content']}\n\n"
            if "hinglish" in r:
                with st.expander("📌Hinglish"):
                    st.write(r["hinglish"])
                    all_text += f"Post {i+1} (Hinglish)\n{r['hinglish']}\n\n"
            st.markdown('</div>', unsafe_allow_html=True)
        st.download_button(
            "⬇️ Download All Posts",
            all_text,
            file_name="linkedin_posts.txt"
        )
st.markdown("---")
st.info("💡 Tip: Copy and post directly on LinkedIn for best engagement 🚀")