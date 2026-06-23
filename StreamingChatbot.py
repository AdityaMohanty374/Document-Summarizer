from openai import OpenAI

client = OpenAI(
        base_url = "http://localhost:11434/v1",
        api_key="dummy",
    )
messages = [{
    "role":"system",
    "content":"You are a strict and disciplined teacher "
}]

while True:
    user = input("You: ")
    messages.append({
        "role":"user",
        "content":user
    })
    stream = client.chat.completions.create(
        model="qwen3:1.7b",
        messages=messages,
        stream=True
    )
    answer=""
    print("Bot: ", end="")
    for chunk in stream:
        if chunk.choices[0].delta.content:
            token=chunk.choices[0].delta.content
            answer+=token
            print(token, end="", flush=True)
    print()

    messages.append({
        "role":"assistant",
        "content":answer
    })
    
