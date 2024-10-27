import os
import requests
import json

# Retrieve the OpenRouter API key from environment variables
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

def call_openrouter_api(prompt: str) -> dict:
    """
    Calls the OpenRouter API with the provided prompt and returns the response.

    Args:
        prompt (str): The prompt to send to the OpenRouter API.

    Returns:
        dict: The JSON response from the API, or an error message if the request fails.
    """
    url = "https://openrouter.ai/api/v1/chat/completions"

    # Set up the headers for the API request
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    # Prepare the data payload for the API request
    data = json.dumps({
        "model": "meta-llama/llama-3-8b-instruct:free",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    })

    # Make the POST request to the OpenRouter API
    response = requests.post(url, headers=headers, data=data)

    # Check the response status and return the appropriate result
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Sorry, I couldn't find an answer to your question."}

def answer_question(text: str, question: str) -> str:
    """
    Generates an answer to a question based on the provided text.

    Args:
        text (str): The text to base the answer on.
        question (str): The question to answer.

    Returns:
        str: The answer to the question, or an error message if the answer cannot be generated.
    """
    # Create a prompt for the OpenRouter API
    prompt = f"Based on the following text, answer the question:\n\nText: {text}\n\nQuestion: {question}"
    
    # Call the OpenRouter API with the generated prompt
    response = call_openrouter_api(prompt)
    
    # Extract and return the answer from the API response
    if "choices" in response and len(response["choices"]) > 0:
        return response["choices"][0]["message"]["content"]
    else:
        return response.get("error", "An unknown error occurred.")
