from openai import OpenAI
import fitz

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="dummy"
)
system_prompt={
    "role":"system",
    "content":"You are a highly capable AI tutor, programmer, researcher, and text summarization assistant. Your goal is to provide accurate, clear, and useful responses tailored to the user's level of understanding. Explain concepts in a way that ranges from beginner-friendly to advanced when needed, using examples, analogies, and step-by-step breakdowns to make complex ideas easier to understand. Always answer the user's question directly before providing additional context or details. For programming-related questions, provide clean, correct, and well-structured code along with explanations of how the code works and why it is written that way. For technical topics, focus on building intuition and practical understanding before diving into theory. When summarizing text or documents, preserve all important information while reducing unnecessary detail and complexity. For long documents, structure summaries with an Executive Summary, Key Points, Important Details, and Action Items when applicable. Always strive to be factual and reliable, clearly acknowledge uncertainty when information is incomplete, and never invent facts. Prioritize clarity over complexity, maintain a logical structure, and present information in a concise, readable, and organized manner."
}
messages = [system_prompt]
def extract_pdf_text(file_path) -> str:
    file_path = file_path.strip('"')
    text=""
    try:
        with fitz.open(file_path) as doc:
            text = "\f".join(page.get_text() for page in doc)
    except Exception as e:
        print(f"Error: {e}")
        return
    return text

def stream_response(messages) -> str:
    ans=""
    stream = client.chat.completions.create(
        model="qwen3:1.7b",
        messages=messages,
        stream=True,
        temperature=0.2,
        top_p=0.9
    )
    for chunk in stream:
        if chunk.choices[0].delta.content:
            token=chunk.choices[0].delta.content
            print(token, end="",flush=True)
            ans+=token
    print()
    return ans

def summarize_text(text):
    return {
        "role": "user",
        "content": f"Summarize:\n\n{text}"
    }

def chat(messages, user):
    messages.append({
        "role":"user",
        "content": user
    })

def clear_chat(messages):
    messages.clear()
    messages .append(system_prompt)
    print("Chat Cleared")

def exit_chat():
    print("Chat Ended")

def main():
    print("Welcome to qwen, to summarize a document enter \"~\", \"clear\" to clear chat, \"exit\" to end chat")
    while True:
        user = input(">>")
        if user=="~":
            file_path=input("Paste the pdf path here: ")
            text=extract_pdf_text(file_path=file_path)
            if text is None:
                continue
            messages.append(summarize_text(text=text))
        elif user.lower()=="clear":
            clear_chat(messages=messages)
            continue
        elif user.lower()=="exit":
            exit_chat()
            break
        else:
            chat(messages=messages, user=user)
        ans = stream_response(messages=messages)
        messages.append({
            "role": "assistant",
            "content": ans
        })

if __name__ == "__main__":
    main()
