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

# --- CUSTOM STYLING (black-white professional look) ---
st.markdown("""
    <style>
        /* Main background and font */
        body {
            background-color: #ffffff;
            color: #000000;
            font-family: 'Poppins', sans-serif;
        }

        /* Center content and add card effect */
        .block-container {
            max-width: 850px;
            margin: auto;
            padding: 3rem 3rem;
            background-color: #ffffff;
        }

        /* Header */
        h1 {
            text-align: center;
            color: #000000;
            font-weight: 700;
            font-size: 2.2rem;
            letter-spacing: -0.5px;
        }

        p, label, textarea, .stTextInput, .stFileUploader label {
            color: #111111 !important;
            font-size: 1rem;
        }

        /* File uploader area */
        .stFileUploader {
            background-color: #fafafa;
            border: 1px solid #000;
            border-radius: 10px;
            padding: 1rem;
        }

        /* Button styling */
        .stButton>button {
            background-color: #000000;
            color: #ffffff;
            border: none;
            border-radius: 8px;
            padding: 0.7rem 1.3rem;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.2s ease;
        }
        .stButton>button:hover {
            background-color: #333333;
            transform: scale(1.03);
        }

        /* Textarea */
        .stTextArea textarea {
            background-color: #ffffff;
            color: #000000;
            border: 1px solid #000;
            border-radius: 8px;
            font-size: 0.95rem;
        }

        /* Info and success boxes */
        .stAlert {
            border-radius: 8px !important;
            font-size: 0.95rem;
        }

        /* Result card */
        .result-box {
            background-color: #f9f9f9;
            border: 1px solid #000;
            border-radius: 12px;
            padding: 1.5rem;
            margin-top: 1rem;
            color: #000000;
        }

        /* Divider */
        hr {
            border: 1px solid #000000;
            margin: 1.5rem 0;
        }

        /* Hide Streamlit default menu and footer for clean look */
        #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1>🤖 AI CV Analyzer (Groq)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#555;'>Upload your CV (PDF) and get instant AI-powered evaluation with Groq LLM</p>", unsafe_allow_html=True)
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
