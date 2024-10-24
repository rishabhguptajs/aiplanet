import os
import requests
import json

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

def call_openrouter_api(prompt: str) -> dict:
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = json.dumps({
        "model": "meta-llama/llama-3-8b-instruct:free",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    })

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Sorry, I couldn't find an answer to your question."}
    

def answer_question(text: str, question: str) -> str:
    prompt = f"Based on the following text, answer the question:\n\nText: {text}\n\nQuestion: {question}"
    response = call_openrouter_api(prompt)
    
    if "choices" in response and len(response["choices"]) > 0:
        return response["choices"][0]["message"]["content"]
    else:
        return response.get("error", "An unknown error occurred.")


sample_text = "LangChain is a framework for developing applications powered by language models. It provides tools for chains, agents, and prompts that can be easily customized for different applications, such as chatbots and document analysis."
sample_question = "What are the uses of LangChain?"

# Get the answer
answer = answer_question(sample_text, sample_question)
print(f"Question: {sample_question}")
print(f"Answer: {answer}")