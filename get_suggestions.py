import time
import random
import openai
import streamlit as st

client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def get_resume_feedback(resume_text, jd_text):
    max_retries = 5
    base_delay = 45

    for attempt in range(max_retries):
        try:
            if attempt > 0:
                # Exponential backoff with jitter
                delay = base_delay * (2 ** (attempt - 1)) + random.uniform(1, 5)
                print(f"Waiting {delay:.1f} seconds before retry {attempt}/{max_retries}")
                time.sleep(delay)

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
            print(f"OpenAI rate limit hit (attempt {attempt + 1}/{max_retries})")

        except Exception as e:
            print(f"Error during GPT call: {e}")
            break  # Stop retrying for unknown errors

    return "⚠ GPT feedback unavailable due to rate limits."
