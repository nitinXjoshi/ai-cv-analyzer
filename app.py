import os
import streamlit as st
import pdfplumber
from dotenv import load_dotenv
from groq import Groq

# Load API key
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("❌ GROQ_API_KEY not found. Please add it in Streamlit Secrets.")
else:
    client = Groq(api_key=api_key)

    st.set_page_config(page_title="AI CV Analyzer (Groq)", layout="centered")
    st.title("🤖 AI CV Analyzer (Groq)")
    st.write("Upload your CV (PDF) and get instant AI feedback!")

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
