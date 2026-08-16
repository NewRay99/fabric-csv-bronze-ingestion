import os
from dotenv import load_dotenv
from openai import OpenAI

# Load key-value pairs from .env into environment variables
load_dotenv()

# Access environment variable
tokenroute_api = os.getenv("TOKENROUTER_API_KEY")

# Check if key was loaded successfully
if not tokenroute_api:
    raise ValueError("TOKENROUTER_API_KEY not found in .env file.")

# Pass the string directly (without curly braces)
client = OpenAI(
    base_url='https://api.tokenrouter.com/v1',
    api_key=tokenroute_api,
)

messages = [
    {"role": "system", "content": "You are an intelligent assistant, please reply concisely."},
    {"role": "user", "content": "Hello, what kind of model are you?"},
]

stream = client.chat.completions.create(
    model="moonshotai/kimi-k3-free",
    messages=messages,
    stream=True,
    stream_options={"include_usage": True},
    extra_body={}
)

content_parts = []
for chunk in stream:
    if chunk.choices:
        delta = chunk.choices[0].delta
        if delta and delta.content:
            content_parts.append(delta.content)

full_content = "".join(content_parts)

print(full_content)