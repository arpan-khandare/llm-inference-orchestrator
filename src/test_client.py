import ollama

def stream_response(prompt: str):
    print(f"Prompt: {prompt}\nResponse: ", end="", flush=True)
    
    # We call the local ollama instance with streaming enabled
    response = ollama.generate(
        model='llama3:8b',
        prompt=prompt,
        stream=True
    )
    
    # Iterate through the tokens as they arrive in real-time
    for chunk in response:
        print(chunk['response'], end="", flush=True)
    print("\n")

if __name__ == "__main__":
    stream_response("Explain matrix multiplication in one sentence.")