import time
import openai
import streamlit as st

client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def get_resume_feedback(resume_text, jd_text):
    max_retries = 3

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional resume reviewer. Compare resumes to job descriptions and suggest improvements."
                    },
                    {
                        "role": "user",
                        "content": f"""
Here is the candidate's resume:
{resume_text}

Here is the job description:
{jd_text}

Please provide detailed suggestions to improve the resume so it aligns better with the job description.
"""
                    }
                ],
                temperature=0.7
            )

            return response.choices[0].message.content

        except openai.RateLimitError:
            print(f"Rate limit hit. Retrying in 10 seconds... (Attempt {attempt + 1}/{max_retries})")
            time.sleep(10)

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break  # Stop retrying on unknown errors

    return "⚠️ We're currently sending too many requests to OpenAI. Please try again later."
