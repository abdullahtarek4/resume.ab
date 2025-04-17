import time
import openai
import streamlit as st
import traceback

client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def get_resume_feedback(resume_text, jd_text):
    max_retries = 5
    base_delay = 30
    MAX_LENGTH = 3000  

    # Input validation
    if not resume_text.strip() or not jd_text.strip():
        return "⚠ Resume or job description is missing."

    # Truncate long inputs
    resume_text = resume_text[:MAX_LENGTH]
    jd_text = jd_text[:MAX_LENGTH]

    for attempt in range(max_retries):
        try:
            if attempt > 0:
                wait_time = base_delay * attempt
                print(f"⏳ Waiting {wait_time} seconds before retrying... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)

            print(f"📤 Attempt {attempt + 1} to call OpenAI API...")
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
            print(f"🚫 Rate limit hit. (Attempt {attempt + 1}/{max_retries})")

        except Exception as e:
            print("❌ Unexpected error during GPT call:")
            traceback.print_exc()
            break  # Stop retrying on unknown errors

    return "⚠ GPT feedback unavailable due to rate limits."
