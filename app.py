import os
import streamlit as st
import pdfplumber
from dotenv import load_dotenv
from groq import Groq

# Load API key
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AI CV Analyzer (Groq)",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM STYLING (Black outer + White container) ---
st.markdown("""
    <style>
        /* Global background and typography */
        body {
            background-color: #000000;
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Poppins', sans-serif;
            color: #000000;
        }

        /* White centered container with subtle shadow */
        .block-container {
            background-color: #ffffff;
            border-radius: 20px;
            padding: 3rem;
            max-width: 850px;
            margin: 3rem auto;
            box-shadow: 0 0 40px rgba(255, 255, 255, 0.05), 0 0 80px rgba(0, 0, 0, 0.3);
        }

        /* Header styling */
        h1 {
            text-align: center;
            color: #000000;
            font-weight: 700;
            font-size: 2.3rem;
            letter-spacing: -0.5px;
        }

        p, label, textarea, .stTextInput, .stFileUploader label {
            color: #000000 !important;
            font-size: 1rem;
        }

        /* File uploader */
        .stFileUploader {
            background-color: #f8f8f8;
            border: 1px solid #000000;
            border-radius: 12px;
            padding: 1rem;
        }

        /* Text area */
        .stTextArea textarea {
            background-color: #ffffff;
            color: #000000 !important;
            border: 1px solid #000000;
            border-radius: 10px;
            font-size: 0.95rem;
        }

        /* Buttons - clean black & white */
        .stButton>button {
            background-color: #000000;
            color: #ffffff;
            border: none;
            border-radius: 10px;
            padding: 0.75rem 1.6rem;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.2s ease;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }

        .stButton>button:hover {
            background-color: #333333;
            transform: translateY(-2px);
        }

        /* Info & success alerts */
        .stAlert {
            border-radius: 10px !important;
            font-size: 0.95rem;
        }

        /* Result box */
        .result-box {
            background-color: #ffffff;
            border: 1.5px solid #000000;
            border-radius: 16px;
            padding: 1.5rem;
            margin-top: 1rem;
            color: #000000;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        }

        /* Divider */
        hr {
            border: 1px solid #000000;
            margin: 1.5rem 0;
        }

        /* Hide Streamlit branding */
        #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1>🤖 AI CV Analyzer (Groq)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#111;'>Upload your CV (PDF) and get instant AI-powered evaluation with Groq LLM</p>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# --- BACKEND LOGIC (unchanged) ---
if not api_key:
    st.error("❌ GROQ_API_KEY not found. Please add it in Streamlit Secrets.")
else:
    client = Groq(api_key=api_key)

    uploaded_file = st.file_uploader("📄 Upload your CV (PDF only)", type=["pdf"])

    if uploaded_file is not None:
        text = ""
        try:
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        except Exception as e:
            st.error(f"❌ Error reading PDF: {e}")

        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader("🧾 Extracted CV Text (Preview)")
        st.text_area(
            "CV Text",
            text[:2000] + ("..." if len(text) > 2000 else ""),
            height=200
        )

        st.markdown("<hr>", unsafe_allow_html=True)

        if st.button("🚀 Analyze CV"):
            st.info("Analyzing your CV... please wait ⏳")

            prompt = f"""
            You are an expert HR recruiter. Evaluate this candidate’s CV for a software engineering role.
            Mention strengths, weaknesses, and rate suitability out of 10.
            CV text:
            {text}
            """

            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                )
                answer = response.choices[0].message.content

                st.success("✅ Analysis complete!")
                st.subheader("🧠 AI Evaluation")
                st.markdown(f"<div class='result-box'>{answer}</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Groq API Error: {e}")
