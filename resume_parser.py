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

def clean_text(text):
    return re.sub(r'[|•–—▪●]', ' ', text)

def extract_email(text):
    text = clean_text(text)
    emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
    print("Emails Found:", emails)
    return emails[0] if emails else None

def extract_phone(text):
    text = clean_text(text)
    phones = re.findall(r'(?:\+?\d{1,3})?[ -]?\(?\d{2,4}\)?[ -]?\d{3,4}[ -]?\d{3,4}', text)
    for phone in phones:
        digits = re.sub(r'\D', '', phone)
        if 10 <= len(digits) <= 15:
            return phone.strip()
    return None

def extract_skills(text, skill_list):
    text = text.lower()
    words = re.findall(r'\w+', text)
    found = [skill for skill in skill_list if skill.lower() in words]
    return list(set(found))
