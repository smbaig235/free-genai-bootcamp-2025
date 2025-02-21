import requests
import json 

def gen_comp(prompt, model="llama3.2:1b"):
    """
    Using Ollama's API to generate completion with streaming support
    """
    url = "http://localhost:8008/api/generate"

    data = {
        "model": model,
        "prompt": prompt,
        "stream": True,
    }

    full_response = ""
    response = requests.post(url, json=data, stream=True)
    
    for line in response.iter_lines():
        if line:
            json_response = json.loads(line)
            chunk = json_response.get("response", "")
            full_response += chunk
            # Print each chunk as it arrives (optional)
            print(chunk, end="", flush=True)
    
    return full_response

def extract_response(response_text):
    """
    Extract just the text response from the Ollama API response
    """
    return response_text

# chat:1
result = gen_comp("what is the capital of France?")
print("\n\nFull response:")
print(result)

# chat:2
result = gen_comp("what object oriented language?")
print("\n\nFull response:")
print(result)

# chat:3
result = gen_comp("what is the color of USA flag?")
print("\n\nFull response:")
print(result)

