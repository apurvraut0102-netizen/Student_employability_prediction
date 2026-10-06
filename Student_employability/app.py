
import pickle
from pathlib import Path
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Neha Lutade | Employability Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

MODEL_PATH = Path(__file__).parent / "model" / "employability_model.pkl"
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #f7f9fc 0%, #eef3ff 55%, #fdf5ff 100%); color: #111827; }
    .stApp p, .stApp label, .stApp span, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 { color: #111827; }
    .hero { padding: 28px 34px; border-radius: 24px; background: linear-gradient(120deg, #111827, #312e81, #7c3aed); color: white; margin-bottom: 22px; box-shadow: 0 14px 35px rgba(49,46,129,.18); }
    .hero h1 { margin: 0; font-size: 38px; color: white !important; }
    .hero p { margin: 8px 0 0; opacity: .88; font-size: 16px; color: white !important; }
    .card { padding: 20px; border-radius: 18px; background: rgba(255,255,255,.95); border: 1px solid rgba(99,102,241,.12); box-shadow: 0 8px 24px rgba(31,41,55,.06); }
    .stSlider label, .stNumberInput label, .stSlider [data-testid="stMarkdownContainer"] p { color: #111827 !important; font-weight: 600 !important; }
    .stNumberInput input { color: #111827 !important; background-color: #ffffff !important; caret-color: #111827 !important; }
    .stSlider [data-baseweb="slider"] { color: #111827 !important; }
    section[data-testid="stSidebar"] { background: #ffffff; }
    section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span, section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3, section[data-testid="stSidebar"] label { color: #111827 !important; }
    .stButton > button { color: white !important; background: linear-gradient(90deg, #4f46e5, #7c3aed); border: none; border-radius: 12px; font-weight: 700; padding: 12px; }
    .stButton > button:hover { color: white !important; background: linear-gradient(90deg, #4338ca, #6d28d9); }
    .result { padding: 24px; border-radius: 20px; text-align: center; margin-top: 18px; background: white; color: #111827 !important; box-shadow: 0 10px 30px rgba(31,41,55,.08); }
    .result h2 { margin: 4px 0 8px; color: #111827 !important; }
    .result p { color: #475569 !important; }
    div[data-testid="stMetric"] { background: white; border-radius: 16px; padding: 10px; box-shadow: 0 6px 18px rgba(31,41,55,.05); }
    div[data-testid="stMetric"] label { color: #64748b !important; }
    div[data-testid="stMetricValue"] { color: #111827 !important; }
    div[data-testid="stAlert"] p { color: #1e293b !important; }
    .small { color: #64748b !important; font-size: 13px; }
    [data-testid="stCaptionContainer"] { color: #64748b !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🎓 Student Employability Predictor</h1>
    <p>Neha Lutade • Machine Learning Project</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## About the project")
    st.write(
        "This application estimates a student's employability using academic, "
        "skill, internship and aptitude indicators."
    )
    st.markdown("---")
    st.markdown("**Model:** Random Forest")
    st.markdown("**Output:** Employable / Needs Development")
    st.markdown("---")
    st.caption("Developed by Neha Lutade")

st.markdown("### Enter student profile")
st.caption("Use the controls below and click **Predict Employability**.")

left, right = st.columns(2)

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    cgpa = st.slider("CGPA", 4.5, 10.0, 7.5, 0.1)
    attendance = st.slider("Attendance (%)", 45, 100, 80)
    internships = st.number_input("Internships completed", 0, 4, 1)
    projects = st.number_input("Projects completed", 0, 6, 2)
    certifications = st.number_input("Certifications", 0, 8, 2)
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    communication = st.slider("Communication skill (1–10)", 1, 10, 7)
    technical = st.slider("Technical skill (1–10)", 1, 10, 7)
    aptitude = st.slider("Aptitude score", 20, 100, 70)
    backlogs = st.number_input("Current/previous backlogs", 0, 6, 0)
    experience = st.number_input("Relevant work experience (years)", 0, 3, 0)
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")
if st.button("🔮 Predict Employability", type="primary", use_container_width=True):
    data = pd.DataFrame([{
        "CGPA": cgpa,
        "Attendance": attendance,
        "Internships": internships,
        "Projects": projects,
        "Certifications": certifications,
        "Communication_Score": communication,
        "Technical_Score": technical,
        "Aptitude_Score": aptitude,
        "Backlogs": backlogs,
        "Work_Experience": experience
    }])

    probability = float(model.predict_proba(data)[0][1])
    prediction = int(model.predict(data)[0])

    if prediction == 1:
        label = "Highly Employable"
        emoji = "🚀"
        message = "The profile shows strong employability indicators."
    else:
        label = "Needs Development"
        emoji = "📚"
        message = "Improving skills, experience and academic indicators could strengthen the profile."

    st.markdown(f"""
    <div class="result">
        <div style="font-size:42px">{emoji}</div>
        <h2>{label}</h2>
        <p>{message}</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Employability probability", f"{probability*100:.1f}%")
    c2.metric("CGPA", f"{cgpa:.2f}")
    c3.metric("Technical skill", f"{technical}/10")

    st.progress(probability)
    st.info(
        "Note: This is an educational prediction model trained on synthetic sample data. "
        "It should not be used for actual hiring decisions."
    )

st.markdown("---")
st.markdown(
    '<div style="text-align:center" class="small">Student Employability Prediction • Neha Lutade • College Project</div>',
    unsafe_allow_html=True
)
