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
role = "user"
prompt = "Suggest me a name for my clothing company (names should be in one word)."

# SYSTEM ROLE
message_system = {
    "role": "system",
    "content": "You are a brand manager who suggests name for companies."
}

# message requires role and content 
message = {
    "role" : role,
    "content" : prompt
}

messages = [message_system, message]

# Temperature by default is 0 - meaning safe or less creativity 

response = client.chat.completions.create(model = model, messages = messages, temperature = 0)
# print(response)

print("\n")

answer = response.choices[0].message.content
print(answer)