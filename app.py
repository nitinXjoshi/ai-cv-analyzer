import os
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
    page_icon="🤖",
    layout="wide",
)

# ===========================
# 🎨 CUSTOM LIGHT THEME (Apple / Notion Style)
# ===========================
st.markdown("""
<style>
/* Global font and layout */
html, body, [class*="st-"] {
    font-family: "Inter", "Segoe UI", sans-serif;
    color: #111111 !important;
    background-color: #ffffff !important;
}

/* Background gradient */
.stApp {
    background: linear-gradient(135deg, #ffffff 0%, #f6f8fb 100%) !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #f4f6fb !important;
    border-right: 1px solid #e0e6ef !important;
}
section[data-testid="stSidebar"] * {
    color: #111111 !important;
}

/* File uploader */
[data-testid="stFileUploader"] section {
    background-color: #ffffff !important;
    border: 2px dashed #007aff !important;
    border-radius: 12px !important;
    color: #111111 !important;
    padding: 1.5rem !important;
}
[data-testid="stFileUploader"] section:hover {
    border-color: #3399ff !important;
}

/* Headings */
h1, h2, h3, h4 {
    color: #000000 !important;
    font-weight: 700;
}

/* Buttons */
.stButton>button {
    background-color: #007aff !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    padding: 0.7rem 1.5rem !important;
    border: none !important;
    transition: 0.2s ease;
}
.stButton>button:hover {
    background-color: #3399ff !important;
    transform: scale(1.03);
}

/* Text area */
textarea {
    background-color: #ffffff !important;
    color: #111111 !important;
    border: 1px solid #d3d8e0 !important;
    border-radius: 10px !important;
    padding: 10px !important;
}

/* Expander */
.stExpander {
    background-color: #ffffff !important;
    color: #111111 !important;
    border: 1px solid #e2e6ed !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}

/* Info, warning, success boxes */
.stAlert {
    border-radius: 10px !important;
    border: 1px solid #e0e6ef !important;
    background-color: #f8faff !important;
    color: #111111 !important;
}

/* Hide default footer and menu */
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
st.sidebar.caption("Made with ❤️ by HireSight")

# ===========================
# 🧩 HEADER
# ===========================
st.markdown("<h1 style='text-align:center;'>🤖 HireSight CV Analyzer (Groq-Powered)</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#333;'>Upload your CV and receive instant AI feedback for job readiness.</h3>", unsafe_allow_html=True)

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
                Format the output professionally in bullet points.

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

                    st.subheader("🧾 AI Evaluation Report")
                    st.markdown("---")
                    st.markdown(f"<div style='color:#111111; font-size:16px; line-height:1.6;'>{answer.replace('**', '')}</div>", unsafe_allow_html=True)
                    st.markdown("---")

                    st.success("✅ Analysis complete!")

                except Exception as e:
                    st.error(f"Groq API Error: {e}")
else:
    st.info("⬆️ Please upload a PDF resume to begin.")
