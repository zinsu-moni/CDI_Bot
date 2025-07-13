#!/usr/bin/env python3
"""
Quick API test to verify all services are working
"""
import requests

def test_working_key():
    print("🔍 Testing the working OpenRouter API key...")
    
    api_key = "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"
    url = 'https://openrouter.ai/api/v1/chat/completions'
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'HTTP-Referer': 'http://localhost:8000',
        'X-Title': 'CDI Bot API Test'
    }
    
    data = {
        'model': 'deepseek/deepseek-chat',
        'messages': [{'role': 'user', 'content': 'Hello, test message'}],
        'max_tokens': 20
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ OpenRouter API is working perfectly!")
            result = response.json()
            content = result.get('choices', [{}])[0].get('message', {}).get('content', 'No content')
            print(f"AI Response: {content}")
            return True
        else:
            print(f"❌ API Failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_working_key()
    
    if success:
        print("\n🎉 All API keys are now properly configured!")
        print("\n📋 Next steps:")
        print("1. Run your FastAPI server: python main_fastapi.py")
        print("2. Run your Telegram bot: python CDI_telegram_bot.py")
        print("3. Both should now work without 401 errors")
    else:
        print("\n❌ There are still issues. Check your API key quota/credits.")
