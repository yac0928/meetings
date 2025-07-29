import requests

def analyze_transcript_with_ollama(transcript_text):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3",
        "prompt": f"請根據以下逐字稿產生會議重點摘要：\n{transcript_text}"
    }
    response = requests.post(url, json=payload)
    result = response.json()
    return result.get("response", "")
