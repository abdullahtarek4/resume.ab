from fpdf import FPDF
import os

def generate_pdf(email, phone, skills, jd_skills, match_score, missing_skills, gpt_feedback):
    pdf = FPDF()
    pdf.add_page()

    font_path = "DejaVuSans.ttf"
    if not os.path.exists(font_path):
        raise FileNotFoundError("DejaVuSans.ttf not found. Please download and place it in your project directory.")

    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.set_font("DejaVu", size=12)

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

    # Return as binary without encoding to latin-1
    return pdf.output(dest='S').encode('utf-8')
