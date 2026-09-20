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

# Structure it

from pydantic import BaseModel

class Ticket(BaseModel):
    name: str
    email: str
    issue: str

schema = Ticket.model_json_schema()

response_format = {
    "type": "json_object"
}

system_prompt = f"""
Extract the personal information from the ticket based on this schema and give me a json output.
{schema}
"""

message_system = {
    "role": "system",
    "content": system_prompt
}


text = "Hello, my name is XYZ. I have an iphone which is not working at all. My adress is Lucknow. My email is abc@gmail.com. My contact number is 8965412365."

prompt = f"""
This is a customer ticket. Please extract the personal information from this.
{text}
"""

# message requires role and content 
message = {
    "role" : role,
    "content" : prompt
}

messages = [message_system, message]

response = client.chat.completions.create(model = model, messages = messages, response_format = response_format)

print("\n")

answer = response.choices[0].message.content
print(answer)

# How to read it (json format)

import json
raw_json = answer

data_file = json.loads(raw_json)

ticket = Ticket(**data_file)

# We can pass this forward 

print(ticket.name)
print(ticket.email)
print(ticket.issue)