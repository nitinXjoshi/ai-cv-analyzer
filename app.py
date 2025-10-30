import os
import re
import streamlit as st
import pdfplumber
from dotenv import load_dotenv
from groq import Groq

# ===========================
# 🔑 LOAD ENV VARIABLES
# ===========================
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# ===========================
# ⚙️ PAGE CONFIG
# ===========================
st.set_page_config(
    page_title="HireSight CV Analyzer",
    page_icon="👥",
    layout="wide",
)

# ===========================
# 🎨 CUSTOM LIGHT THEME (Apple / Notion Style)
# ===========================
st.markdown("""
<style>
:root, html, body, [class*="st-"] {
    --background-color: #ffffff !important;
    --text-color: #111111 !important;
    color-scheme: light !important;
}

html, body, [class*="st-"] {
    font-family: "Inter", "Segoe UI", sans-serif;
    color: var(--text-color);
    background-color: var(--background-color);
}

.stApp {
    background: linear-gradient(135deg, #ffffff 0%, #f9fbff 100%) !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #f7f9fc !important;
    border-right: 1px solid #e3e8ef !important;
}
section[data-testid="stSidebar"] * {
    color: #111 !important;
}

/* File uploader */
[data-testid="stFileUploader"] section {
    background-color: #ffffff !important;
    border: 2px dashed #007aff !important;
    border-radius: 12px !important;
    color: #111111 !important;
    padding: 1.2rem !important;
}
[data-testid="stFileUploader"] section:hover {
    border-color: #3399ff !important;
    background-color: #f5f9ff !important;
}

/* Buttons */
.stButton>button {
    background-color: #007aff !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.2rem !important;
    border: none !important;
    transition: 0.2s ease;
}
.stButton>button:hover {
    background-color: #3399ff !important;
    transform: scale(1.03);
}

/* Text Area */
textarea {
    background-color: #ffffff !important;
    color: #111111 !important;
    border: 1px solid #cfd6e3 !important;
    border-radius: 10px !important;
    padding: 10px !important;
}

/* Alerts, expanders, text boxes */
.stAlert, .stExpander {
    background-color: #ffffff !important;
    border: 1px solid #e3e8ef !important;
    border-radius: 10px !important;
    color: #111 !important;
}

/* Headings */
h1, h2, h3, h4, h5 {
    color: #000000 !important;
    font-weight: 700 !important;
}

/* Hide Streamlit branding */
#MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ===========================
# 🧭 SIDEBAR
# ===========================
st.sidebar.title("⚙️ Control Panel")
st.sidebar.write("Use this sidebar to navigate.")
st.sidebar.markdown("---")
st.sidebar.info("💡 Upload your CV in PDF format and click **Analyze CV** to get instant AI-powered feedback.")
st.sidebar.markdown("---")
st.sidebar.caption("Made with ❤️ by Team CodeStuds")

# ===========================
# 🧩 HEADER
# ===========================
st.markdown("<h1 style='text-align:center;'>HireSight Resume Analyzer (Groq-Powered)</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#333;'>Upload Resume.</h3>", unsafe_allow_html=True)

# ===========================
# 🔍 API CHECK
# ===========================
if not api_key:
    st.error("❌ GROQ_API_KEY not found. Please add it to your Streamlit secrets or .env file.")
    st.stop()

client = Groq(api_key=api_key)

# ===========================
# 📤 CV UPLOAD SECTION
# ===========================
col1, col2 = st.columns([1.2, 2])

with col1:
    st.subheader("📄 Upload CV")
    uploaded_file = st.file_uploader("Choose your CV (PDF only)", type=["pdf"])

with col2:
    st.subheader("🧠 About This Tool")
    st.markdown("""
    - Extracts and reads your CV text using AI  
    - Evaluates your **strengths and weaknesses**  
    - Suggests **improvements**  
    - Gives you a **suitability score out of 10**
    """)

# ===========================
# 🧾 CV EXTRACTION
# ===========================
if uploaded_file is not None:
    text = ""
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    except Exception as e:
        st.error(f"❌ Error reading PDF: {e}")

    if text.strip() == "":
        st.error("⚠️ Could not extract any text from the uploaded file.")
    else:
        st.success("✅ CV extracted successfully!")

        with st.expander("🔍 Preview Extracted Text"):
            st.text_area("Extracted CV Text", text[:2500] + ("..." if len(text) > 2500 else ""), height=250)

        # ===========================
        # 🚀 ANALYZE BUTTON
        # ===========================
        if st.button("🚀 Analyze CV", use_container_width=True):
            with st.spinner("Analyzing your CV using Groq AI... ⏳"):
                prompt = f"""
                You are an expert HR recruiter evaluating a candidate for a software engineering role.
                Analyze the following CV text. Provide:
                - Key strengths
                - Weaknesses
                - Technical impression
                - Soft skill evaluation
                - Overall suitability rating (out of 10)
                Format the output professionally in bullet points. Do not give asterick in response. Give the overall sustainability score in bold.

                CV:
                {text}
                """
                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                    )
                    answer = response.choices[0].message.content
                    st.balloons()

                    # ===========================
                    # 🧾 AI EVALUATION REPORT (Beautiful Formatting)
                    # ===========================
                    st.subheader("🧾 AI Evaluation Report")
                    st.markdown("---")

                    formatted_answer = re.sub(
                        r"(?i)(strengths|weaknesses|technical impression|soft skill evaluation|overall suitability rating.*?)\s*:",
                        lambda m: f"<h4 style='color:#007aff; margin-top:1rem;'>{m.group(1).title()}:</h4>",
                        answer
                    )

                    formatted_answer = (
                        formatted_answer
                        .replace("•", "👉")
                        .replace("-", "•")
                        .replace("\n", "<br>")
                    )

                    st.markdown(f"""
                    <div style='
                        background-color:#ffffff;
                        border:1px solid #e0e6ef;
                        border-radius:12px;
                        padding:1.5rem;
                        line-height:1.7;
                        font-size:16px;
                        color:#111111;
                    '>
                    {formatted_answer}
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("---")
                    st.success("✅ Analysis complete!")

                except Exception as e:
                    st.error(f"Groq API Error: {e}")
else:
    st.info("⬆️ Please upload a PDF resume to begin.")
