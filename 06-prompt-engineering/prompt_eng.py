import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("API Error")

client = Groq(api_key = my_api_key)

model = "openai/gpt-oss-120b"

def llm_ans(prompt):
    message = {
        "role": "user",
        "content": prompt
    }

    messages = [message]
    response = client.chat.completions.create(model = model, messages = messages)
    ans = response.choices[0].message.content
    return ans

#bad_prompt = """
#This is a user complaint:
#My laptop is not working.
#Classify this.
#"""

#print(llm_ans(bad_prompt))

good_prompt = """

#ROLE: You are a support assistant at a mobil/laptop company.

#TASK: You have to classify the issue in a category.

#CONSTRAINTS: You have to classify the issues in one of the three categories namely - Billing, Technical, Return.

#OUTPUT FORMAT: Your answeer should be in one word only. The one word should be one of the categories given in constraints.

#EXAMPLE: For instance, if a useer complaint says they want a refund then the category is Return.

#FALLBACK: If the issue is unrelated to any of the categories mentioned in the contraints then the answer should be Others.

This is a user complaint:
My laptop is not working.
"""

print(llm_ans(good_prompt))