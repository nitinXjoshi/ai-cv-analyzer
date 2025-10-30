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

# --- PREMIUM DARK UI STYLING ---
st.markdown("""
    <style>
        /* Overall page */
        body {
            background-color: #000000;
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Poppins', sans-serif;
        }

        .block-container {
            max-width: 850px;
            margin: auto;
            padding: 3rem 3rem;
            background-color: transparent;
        }

        /* Header */
        h1 {
            text-align: center;
            color: #f5f5f7;
            font-weight: 700;
            font-size: 2.3rem;
            letter-spacing: -0.5px;
            margin-bottom: 0.5rem;
        }

        p {
            text-align: center;
            color: #a0a0a0;
            font-size: 1rem;
            margin-top: 0rem;
            margin-bottom: 2rem;
        }

        /* Blue-glass containers */
        .card {
            background: linear-gradient(145deg, #0a0f1a, #0d1625);
            border: 1px solid #1e3a8a;
            border-radius: 16px;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
            padding: 1.8rem;
            margin-bottom: 1.5rem;
        }

        /* File uploader */
        .stFileUploader {
            background-color: rgba(30, 64, 175, 0.15);
            border: 1px solid #1e3a8a;
            border-radius: 12px;
            padding: 1rem;
        }

        /* Button styling */
        .stButton>but
