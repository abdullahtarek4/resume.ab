import re
import spacy
from pdfminer.high_level import extract_text
import subprocess
import importlib

# Load the NLP model
try:
    nlp = spacy.load("en_core_web_lg")
except OSError:
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_lg"])
    importlib.invalidate_caches()
    nlp = spacy.load("en_core_web_lg")

def extract_resume_text(file):
    return extract_text(file)

def extract_email(text):
    # Find all emails (better regex)
    emails = re.findall(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', text)
    return emails[0] if emails else None

def extract_phone(text):
    # Match international/local numbers
    phones = re.findall(r'(\+?\d{1,3}[-\s]?)?(\(?\d{2,4}\)?[-\s]?)?\d{6,12}', text)
    if phones:
        # Join tuples and return first valid number
        for phone_tuple in phones:
            phone = ''.join(phone_tuple).replace(" ", "").replace("-", "")
            if len(phone) >= 10:
                return phone
    return None

def extract_skills(text, skill_list):
    skills_found = []
    text = text.lower()
    for skill in skill_list:
        if skill.lower() in text:
            skills_found.append(skill)
    return list(set(skills_found))
