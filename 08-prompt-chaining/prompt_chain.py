import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from time import sleep 

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("API Error")

client = Groq(api_key = my_api_key)

model = "openai/gpt-oss-120b"

JD = """
We are hiring a Backend Python Developer.

Requirements:
- Strong Python
- FastAPI or Django
- PostgreSQL
- Docker
- AWS
- REST APIs
- 2+ years of experience
"""

RESUME = """
Name: Rahul Sharma

Experience: 3 years as a Software Developer

Skills: Python, FastAPI, MySQL, Docker, REST APIs, Git

Projects: Built a food delivery backend using FastAPI and MySQL.

Deployed applications using Docker.
"""

def ask_llm(system_prompt, user_prompt):
    sys_msg = {
        "role": "system",
        "content": system_prompt
    }

    user_msg = {
        "role": "user",
        "content": user_prompt
    }

    messages = [sys_msg, user_msg]
    response = client.chat.completions.create(model = model, messages = messages)
    answer = response.choices[0].message.content
    return answer 

# Extarct skills from the resume
def step1_res_extract():
    system_prompt = """
    You are a professional HR Assistant. Extract the skills from the candidate's resume provided. Only return the skills and no other information. Do not invent any skills by yourself.
    """

    user_prompt = f"""
    Extract the skills from this resume
    {RESUME}
    """

    return ask_llm(system_prompt, user_prompt)

# Extract skills from the JD
def step2_JD_extract():
    system_prompt = """
    You are a professional HR Assistant. Extract the skills from the job description provided. Only return the skills and no other information. Do not invent any skills by yourself.
    """

    user_prompt = f"""
    Extract the skills from this JD
    {JD}
    """

    return ask_llm(system_prompt, user_prompt)

# Match the skills from the resume and the JD
def step3_match(candidate, jd):
    system_prompt = """
    You are a professional HR Assistant. Compare the skills of the candidate and the skills required in the JD and generate a final score between 1 to 100 and also generate a short verdict whether the candidate is a good fit for the role.
    """

    user_prompt = f"""
    Compare and match the skills

    JD: 
    {jd}
    Candidate:
    {candidate}
    """

    return ask_llm(system_prompt, user_prompt)

candidate = step1_res_extract()
sleep(2)
jd = step2_JD_extract()
sleep(2)
score = step3_match(candidate, jd)
print(score)