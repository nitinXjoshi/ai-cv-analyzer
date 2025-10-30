st.markdown("""
<style>
/* App background */
.stApp {
    background: linear-gradient(135deg, #ffffff 0%, #f7f9fc 100%);
    font-family: 'Segoe UI', sans-serif;
    color: #111111;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #f1f4fa;
    color: #000000;
    border-right: 1px solid #d8dee9;
}
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] div {
    color: #000000 !important;
}

/* Headings */
h1, h2, h3 {
    color: #000000 !important;
    font-weight: 700;
}

/* General text */
p, label, .stMarkdown, .stText, div, span {
    color: #222222 !important;
}

/* Card containers */
div[data-testid="stVerticalBlock"] {
    background: #ffffff;
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 4px 25px rgba(0,0,0,0.08);
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

/* Text area (white box, black text) */
textarea {
    border-radius: 10px !important;
    border: 1px solid #cccccc;
    background-color: #ffffff !important;
    color: #000000 !important;
    font-family: 'Courier New', monospace;
    font-size: 14px;
}

/* Expander (Preview box) */
.stExpander {
    background-color: #ffffff !important;
    border: 1px solid #dcdcdc !important;
    border-radius: 12px !important;
    color: #000000 !important;
}

/* Alerts/info boxes */
.stAlert {
    border-radius: 10px;
    color: #111111 !important;
    background-color: #eaf2ff !important;
    border: 1px solid #d1e0ff;
}

/* Hide footer/menu */
#MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)
