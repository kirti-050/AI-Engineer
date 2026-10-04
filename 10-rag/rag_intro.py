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

# Step 1 - Creating Knowledge Base

knowledge_base = {
    "age": "The age of Kirti is 20 years.", 
    "school": "The school Kirti stuided in was Montfort."
}

# Step 2 - Retrieval

def retrieve_info(question):
    question = question.lower()
    if "age" in question:
        return knowledge_base["age"]
    elif "school" in question:
        return knowledge_base["school"]
    else:
        return None 

def ask_llm(question):
    context = retrieve_info(question)

    sys_prompt = f"""Answer in one line only. Answer only based on this context. Do not hallucinate. 
    Context: {context}
    """

    system_message = {
        "role": "system",
        "content": sys_prompt
    }

    user_message = {
        "role": "user",
        "content": question
    }

    messages = [system_message, user_message]

    response = client.chat.completions.create(model = model, messages = messages)

    answer = response.choices[0].message.content

    return answer


question = "What is Kirti's school?"
print(ask_llm(question))