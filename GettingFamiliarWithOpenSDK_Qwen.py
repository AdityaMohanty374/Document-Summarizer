import os 
from openai import OpenAI

full_responses=""

client = OpenAI(
    base_url = "http://localhost:11434/v1",
    api_key="dummy",
)
stream = client.chat.completions.create(
    model="qwen3:1.7b",
    messages=[
        {
            "role":"system",
            "content":"You are an expert and seasoned paragraph summarizer"
        },
        {
            "role":"user",
            "content": "Explain neural networks in 200 words
        }
    ],
    stream=True,
    temperature=0.2,
    top_p=0.9
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        token = chunk.choices[0].delta.content
        full_responses+=token
        print(token, end="", flush=True)


