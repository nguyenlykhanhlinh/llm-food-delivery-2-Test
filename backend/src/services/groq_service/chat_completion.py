from tenacity import retry, wait_random, stop_after_attempt
from groq import Groq


@retry(wait=wait_random(min=1, max=5), stop=stop_after_attempt(5))
async def chat_completion(messages, CONFIG, functions=[], client=None):
    """Receives the chatlog from the user and answers"""

    # Initialize Groq client
    groq_client = Groq(api_key=CONFIG["groq"]["api_key"])

    model_args = {
        "model": "llama-3.1-70b-versatile",
        "messages": messages,
        "temperature": CONFIG["groq"].get("temperature", 0),
        "max_tokens": CONFIG["groq"].get("max_tokens", 512),
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }

    # Add function calling if needed
    if len(functions) > 0:
        model_args["functions"] = functions
        model_args["function_call"] = "auto"

    response = groq_client.chat.completions.create(**model_args)
    return response
