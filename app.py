import os
import streamlit as st
import pdfplumber
from dotenv import load_dotenv
from groq import Groq

# Load API key
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# --- Page config ---
st.set_page_config(page_title="AI CV Analyzer (Groq)", layout="centered")

# --- Minimal style (non-intrusive) ---
st.markdown("""
    <style>
        /* Global background and text */
        body {
            background-color: #ffffff;
            color: #000000;
            font-family: 'Segoe UI', sans-serif;
        }

        /* Center main block slightly */
        .block-container {
            max-width: 800px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        /* Header text */
        h1 {
            text-align: center;
            color: #000;
            font-weight: 700;
        }

        /* Upload area */
        .stFileUploader {
            border: 1px solid #000;
            border-radius: 8px;
            padding: 0.8rem;
            background-color: #f8f8f8;
        }

        /* Buttons */
        .stButton>button {
            background-color: #000000;
            color: white;
            border-radius: 6px;
            border: none;
            font-weight: 600;
            padding: 0.5rem 1rem;
            transition: 0.2s;
        }
        .stButton>button:hover {
            background-color: #333333;
            transform: scale(1.02);
        }

        /* Text area */
        .stTextArea textarea {
            background-color: #ffffff;
            color: #000000;
            border: 1px solid #ccc;
            border-radius: 6px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.title("🤖 AI CV Analyzer (Groq)")
st.write("Upload your CV (PDF) and get instant AI feedback!")

# --- API validation ---
if not api_key:
    st.error("❌ GROQ_API_KEY not found. Please add it in Streamlit Secrets.")
else:
    client = Groq(api_key=api_key)

    # --- File upload ---
    uploaded_file = st.file_uploader("📄 Upload your CV (PDF only)", type=["pdf"])

    if uploaded_file is not None:
        text = ""
        try:
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        except Exception as e:
            st.error(f"❌ Error reading PDF: {e}")

        st.subheader("🧾 Extracted CV Text (Preview)")
        st.text_area("CV Text", text[:2000] + ("..." if len(text) > 2000 else ""), height=200)

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
                st.write(answer)
            except Exception as e:
                st.error(f"Groq API Error: {e}")
