import openai
import os

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_resume_feedback(resume_text, jd_text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that gives feedback on resumes."},
            {"role": "user", "content": f"Resume:\n{resume_text}"},
            {"role": "user", "content": f"Job Description:\n{jd_text}"},
        ],
        temperature=0.7
    )
    return response.choices[0].message.content