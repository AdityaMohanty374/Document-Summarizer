from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import tempfile
import os
import prompts

from llm import (
    extract_pdf_text,
    stream_response,
    summarize_text,
    chat,
    clear_chat
)


app = FastAPI(title="Document Summarizer API")

# Temporary conversation history
messages = [prompts.SYSTEM_PROMPT]


class ChatRequest(BaseModel):
    message: str

def generate_response(messages):

    answer = ""

    for token in stream_response(messages):
        answer += token

    return answer

@app.get("/")
def home():
    return {
        "status": "running",
        "model": "qwen3:1.7b"
    }


@app.post("/chat")
def chat_endpoint(request: ChatRequest):

    chat(messages, request.message)

    answer = generate_response(messages=messages)

    messages.append({
        "role": "assistant",
        "content": answer
    })

    return {
        "response": answer
    }


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp:

        temp.write(await file.read())

        temp_path = temp.name

    try:

        text = extract_pdf_text(temp_path)

        messages.append(
            summarize_text(text)
        )

        answer = generate_response(messages=messages)

        messages.append({
            "role": "assistant",
            "content": answer
        })

        return {
            "summary": answer
        }

    finally:

        os.remove(temp_path)


@app.post("/clear")
def clear():

    clear_chat(messages)

    return {
        "message": "Conversation cleared."
    }
