import streamlit as st
from resume_parser import extract_resume_text, extract_email, extract_phone, extract_skills
from get_suggestions import get_resume_feedback
from report_generator import generate_pdf

st.set_page_config(page_title="Smart Resume Analyzer", layout="wide")

st.markdown(
    """
    <style>
        .main-title {
            font-size:40px !important;
            color:#6C63FF;
            font-weight: 700;
        }
        .sub-title {
            font-size: 18px;
            color: #555;
        }
        .section-header {
            font-size: 22px;
            color: #6C63FF;
            margin-top: 30px;
        }
        .info-box {
            background-color: #f5f7fa;
            padding: 15px;
            border-radius: 12px;
            margin-bottom: 20px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
        }
        .stButton button {
            background-color: #6C63FF;
            color: white;
            border-radius: 10px;
            padding: 8px 20px;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<p class="main-title">Smart Resume Analyzer</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Analyze your resume, match it with job descriptions, and get AI-powered suggestions.</p>', unsafe_allow_html=True)
st.markdown("<hr><center>Made with ❤ by Abdullah Tarek</center>", unsafe_allow_html=True)

skill_list = ["Python", "Java", "C++", "SQL", "TensorFlow", "Pandas", "Flask", "Django", "AWS", "React"]

with st.container():
    st.markdown('<p class="section-header">1. Upload Resume</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    text = extract_resume_text(uploaded_file)
    skills = extract_skills(text, skill_list)

    with st.container():
        st.markdown('<p class="section-header">2. Extracted Information</p>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="info-box">
            <strong>Email:</strong> {extract_email(text)}<br>
            <strong>Phone:</strong> {extract_phone(text)}<br>
            <strong>Skills Detected:</strong> {', '.join(skills) if skills else "No skills found."}
        </div>
        """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<p class="section-header">3. Paste Job Description</p>', unsafe_allow_html=True)
        jd_text = st.text_area("Paste the job description here...")

    if jd_text:
        jd_skills = extract_skills(jd_text, skill_list)
        match_score = int(len(set(skills).intersection(jd_skills)) / len(jd_skills) * 100) if jd_skills else 0
        missing_skills = set(jd_skills) - set(skills)

        st.success(f"*Match Score:* {match_score}%")
        if missing_skills:
            st.warning(f"*Missing Skills:* {', '.join(missing_skills)}")

        feedback = ""
        if st.button("Get AI Suggestions to Improve Resume"):
            with st.spinner("Analyzing with GPT..."):
                feedback = get_resume_feedback(text, jd_text)
            st.subheader("GPT Feedback")
            st.write(feedback)

        if feedback:
            pdf_bytes = generate_pdf(
                extract_email(text),
                extract_phone(text),
                skills,
                jd_skills,
                match_score,
                missing_skills,
                feedback
            )

            st.download_button(
                label="Download PDF Report",
                data=pdf_bytes,
                file_name="resume_analysis_report.pdf",
                mime="application/pdf"
            )
