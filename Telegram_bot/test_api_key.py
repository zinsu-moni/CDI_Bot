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
