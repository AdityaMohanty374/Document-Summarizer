import os 
from openai import OpenAI
import fitz

pdf_path = r"C:\Users\mohan\OneDrive - vit.ac.in\Documents\ML\testExtractFile.pdf"

with fitz.open(pdf_path) as doc:
    text = "\f".join(page.get_text() for page in doc)

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
            "content": text
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


