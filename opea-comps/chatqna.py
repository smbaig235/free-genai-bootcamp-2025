import requests

def gen_comp (prompt, model="llama3.2:1b"):
    """
    by using Ollama's API generating the completion 
    """
    url = "http://localhost:8008/api/generate"

    data = {
        "model": model,
        "prompt": prompt,
        "stream": true, 
    }

    response = requests.post(url, json=data)
    return response.json()

def extract_response(response_json):
    """
    Extract just the text response from the Ollama API response
    """
    return response_json.get("response", "")

result = gen_comp("what is the capital of France?")
print("Full JSON response:")
print(result)

print("\nJust the text response:")
print(extract_response(result))
