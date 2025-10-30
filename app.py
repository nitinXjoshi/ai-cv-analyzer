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
# 🎨 PREMIUM BLACK-BLUE THEME WITH LEGIBLE TEXT
# ===========================
st.markdown("""
<style>
/* Global app background */
.stApp {
    background: linear-gradient(135deg, #000000 0%, #0a0a23 100%);
    font-family: 'Segoe UI', sans-serif;
    color: #f5f5f5;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background-color: #0d0d2a;
    color: #ffffff;
    border-right: 1px solid rgba(255,255,255,0.1);
}
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] div {
    color: #ffffff !important;
}

/* Headings */
h1, h2, h3 {
    color: #ffffff !important;
    font-weight: 700;
}

/* General text and markdown */
p, label, .stMarkdown, .stText, div, span {
    color: #f5f5f5 !important;
}

/* Card containers */
div[data-testid="stVerticalBlock"] {
    background: #1a1a40;
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 4px 25px rgba(0,0,0,0.3);
    margin-top: 1.5rem;
}

/* Buttons */
.stButton>button {
    background: #007aff;
    color: #ffffff;
    border-radius: 10px;
    font-weight: 600;
    transition: 0.2s;
    padding: 0.7rem 1.5rem;
    border: none;
}
.stButton>button:hover {
    background: #3399ff;
    transform: scale(1.03);
}

/* Text area */
textarea {
    border-radius: 10px !important;
    border: 1px solid #666;
    background-color: #ffffff !important;
    color: #000000 !important;
}

/* Expander (Preview box) */
.stExpander {
    background-color: #ffffff !important;
    color: #000000 !important;
}

/* Alerts and info boxes */
.stAlert {
    border-radius: 10px;
    color: #000000 !important;
    background-color: #f5f5f5 !important;
}

/* Hide footer/menu */
#MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ===========================
# 🧭 SIDEBAR
# ===========================
st.sidebar.title("⚙️ Control Panel")
st.sidebar.write("Use this sidebar to navigate.")
st.sidebar.markdown("---")
st.sidebar.info("💡 Tip: Upload your CV in PDF format and click **Analyze CV** to get AI-powered evaluation.")
st.sidebar.markdown("---")
st.sidebar.caption("Made with ❤️ by HireSight")

# ===========================
# 🧩 HEADER
# ===========================
st.markdown("<h1 style='text-align:center;'>🤖 HireSight CV Analyzer (Groq-Powered)</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#cccccc;'>Upload your CV and receive instant AI feedback for your job readiness.</h3>", unsafe_allow_html=True)

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
                    st.markdown(f"<div style='color:#ffffff;'>{answer.replace('**', '')}</div>", unsafe_allow_html=True)
                    st.markdown("---")

                    st.success("✅ Analysis complete!")

                except Exception as e:
                    st.error(f"Groq API Error: {e}")

else:
    st.info("⬆️ Please upload a PDF resume to begin.")
