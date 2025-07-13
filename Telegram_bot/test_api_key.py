import requests
import json

# Test the new API key
api_key = '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'
url = 'https://openrouter.ai/api/v1/chat/completions'

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

data = {
    'model': 'deepseek/deepseek-chat',
    'messages': [{'role': 'user', 'content': 'Hello'}],
    'max_tokens': 10
}

try:
    print("Testing new OpenRouter API key...")
    response = requests.post(url, headers=headers, json=data, timeout=10)
    print(f'Status Code: {response.status_code}')
    if response.status_code == 200:
        print("✅ New API key is valid!")
        result = response.json()
        print(f"Response: {result.get('choices', [{}])[0].get('message', {}).get('content', 'No content')}")
    else:
        print(f"❌ API key failed: {response.text}")
except Exception as e:
    print(f'❌ Error: {e}')
