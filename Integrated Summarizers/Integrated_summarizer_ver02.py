from openai import OpenAI
import fitz
import os

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="dummy"
)
messages = [{
    "role":"system",
    "content": "You are a highly capable AI tutor, programmer, researcher, and text summarization assistant. Your goal is to provide accurate, clear, and useful responses tailored to the user's level of understanding. Explain concepts in a way that ranges from beginner-friendly to advanced when needed, using examples, analogies, and step-by-step breakdowns to make complex ideas easier to understand. Always answer the user's question directly before providing additional context or details. For programming-related questions, provide clean, correct, and well-structured code along with explanations of how the code works and why it is written that way. For technical topics, focus on building intuition and practical understanding before diving into theory. When summarizing text or documents, preserve all important information while reducing unnecessary detail and complexity. For long documents, structure summaries with an Executive Summary, Key Points, Important Details, and Action Items when applicable. Always strive to be factual and reliable, clearly acknowledge uncertainty when information is incomplete, and never invent facts. Prioritize clarity over complexity, maintain a logical structure, and present information in a concise, readable, and organized manner."
}]
system_prompt={
    "role":"user",
    "content":"..."
}
file_path=""
text=""
print("Welcome to qwen, to summarize a document press \"~\"")
while True:
    user=input(">>")
    if user=="~":
        file_path=input("Paste the pdf path here: ")
        file_path=file_path[1:-1] #to remove quotes
        with fitz.open(file_path) as doc:
            print(f"Pages: {len(doc)")
            text = "\f".join(page.get_text() for page in doc)
        messages.append({
            "role":"user",
            "content":"Summarize: "+text
        })
    elif user.lower()=="clear":
        messages=[system_prompt]
        print("Chat Cleared")
        continue
    elif user.lower()=="exit":
        print("Chat ended")
        break
    else:
        messages.append({
            "role":"user",
            "content":user
        })
    stream = client.chat.completions.create(
        model = "qwen3:1.7b",
        messages = messages,
        stream = True,
        temperature = 0.2,
        top_p = 0.9
    )
    ans = ""
    for chunk in stream:
        if chunk.choices[0].delta.content:
            token = chunk.choices[0].delta.content
            ans+=token
            print(token, end="", flush = True)
    print()
    messages.append({
        "role":"assistant",
        "content":ans
    })
