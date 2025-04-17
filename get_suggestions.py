import time
import openai
from openai import RateLimitError

def get_resume_feedback(resume_text, jd_text):
    max_retries = 3
    for i in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional resume reviewer."},
                    {"role": "user", "content": f"Here is a resume:\n{resume_text}\n\nHere is a job description:\n{jd_text}\n\nGive suggestions to improve the resume."}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
        except openai.RateLimitError:
            print(f"Rate limit hit. Retrying in 10 seconds... (Attempt {i + 1})")
            time.sleep(10)
    return "⚠️ Too many requests to OpenAI API. Please try again later."
