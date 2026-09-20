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
prompt = "Do you know Franz Kafka?"
# message requires role and content 
message = {
    "role" : role,
    "content" : prompt
}

messages = [message]

response = client.chat.completions.create(model = model, messages = messages)
print(response)

print("\n")

answer = response.choices[0].message.content
print(answer)