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

# 3 Prompts

prompt1 = "Hi!"
prompt2 = "Explain time travel in detail in 100 words."
prompt3 = "Write a 1000 word essay on Machine Learning"

prompts = [prompt1, prompt2, prompt3]

for prompt in prompts:
    message = {
    "role" : role,
    "content" : prompt
}
    messages = [message]

    response = client.chat.completions.create(model = model, messages = messages, max_tokens = 50)

    usage = response.usage

    print(f"""Prompt: {prompt} --> Your Tokens: {usage.prompt_tokens} Completion Tokens: {usage.completion_tokens} 
          Total Token: {usage.total_tokens} Finish Reason: {response.choices[0].finish_reason}""")

#prompt = "Do you know Franz Kafka?"
# message requires role and content 
# message = {
#    "role" : role,
#    "content" : prompt
#}

#messages = [message]

#response = client.chat.completions.create(model = model, messages = messages)
#print(response)

#print("\n")

#answer = response.choices[0].message.content
#print(answer)