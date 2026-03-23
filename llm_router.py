import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

def get_llm_response(prompt: str, system: str = None) -> str:
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    kwargs = {
        'model': 'claude-haiku-4-5-20251001',
        'max_tokens': 2000,
        'messages': [{'role': 'user', 'content': prompt}]
    }
    if system:
        kwargs['system'] = system
    response = client.messages.create(**kwargs)
    return response.content[0].text
