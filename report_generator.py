from fpdf import FPDF

def generate_pdf(email, phone, skills, jd_skills, match_score, missing_skills, gpt_feedback):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Resume Analysis Report", ln=True, align='C')
    pdf.ln(10)

    pdf.cell(200, 10, txt=f"Email: {email}", ln=True)
    pdf.cell(200, 10, txt=f"Phone: {phone}", ln=True)
    pdf.ln(5)

    pdf.cell(200, 10, txt="Skills Found:", ln=True)
    pdf.multi_cell(0, 10, txt=', '.join(skills))
    pdf.ln(5)

    pdf.cell(200, 10, txt="Job Description Skills:", ln=True)
    pdf.multi_cell(0, 10, txt=', '.join(jd_skills))
    pdf.ln(5)

    pdf.cell(200, 10, txt=f"Match Score: {match_score}%", ln=True)
    pdf.cell(200, 10, txt="Missing Skills:", ln=True)
    pdf.multi_cell(0, 10, txt=', '.join(missing_skills) if missing_skills else "None")
    pdf.ln(5)

    pdf.cell(200, 10, txt="GPT Suggestions:", ln=True)
    pdf.multi_cell(0, 10, txt=gpt_feedback or "No feedback generated.")

    return pdf.output(dest='S').encode('latin-1')