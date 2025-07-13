#!/usr/bin/env python3
"""
Debug script to test all API keys and identify the source of 401 errors
"""

import requests
import json

def test_openrouter_api(api_key, key_name):
    """Test OpenRouter API key"""
    print(f"\n🔍 Testing OpenRouter API Key: {key_name}")
    print(f"Key: {api_key[:20]}...")
    
    url = 'https://openrouter.ai/api/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'HTTP-Referer': 'http://localhost:8000',
        'X-Title': 'CDI Bot Test'
    }
    
    data = {
        'model': 'deepseek/deepseek-chat',
        'messages': [{'role': 'user', 'content': 'Hello'}],
        'max_tokens': 10
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=15)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API key is VALID!")
            try:
                result = response.json()
                content = result.get('choices', [{}])[0].get('message', {}).get('content', 'No content')
                print(f"Response: {content}")
            except:
                print("✅ API key works but couldn't parse response")
        else:
            print(f"❌ API key FAILED!")
            print(f"Error: {response.text}")
            
            # Try to parse error details
            try:
                error_data = response.json()
                print(f"Error details: {json.dumps(error_data, indent=2)}")
            except:
                pass
                
    except Exception as e:
        print(f"❌ Request FAILED: {e}")

def test_telegram_bot(bot_token):
    """Test Telegram Bot API"""
    print(f"\n🤖 Testing Telegram Bot Token")
    print(f"Token: {bot_token[:20]}...")
    
    url = f'https://api.telegram.org/bot{bot_token}/getMe'
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Telegram bot token is VALID!")
            result = response.json()
            if result.get('ok'):
                bot_info = result.get('result', {})
                print(f"Bot name: {bot_info.get('first_name', 'Unknown')}")
                print(f"Username: @{bot_info.get('username', 'Unknown')}")
            else:
                print(f"❌ Telegram API error: {result}")
        else:
            print(f"❌ Telegram bot token FAILED!")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Telegram test FAILED: {e}")

def test_kindwise_api(api_key):
    """Test KindWise API"""
    print(f"\n🌱 Testing KindWise API Key")
    print(f"Key: {api_key[:20]}...")
    
    # Simple API test without image
    url = "https://crop.kindwise.com/api/v1/identification"
    headers = {
        'Content-Type': 'application/json',
        'Api-Key': api_key
    }
    
    # Test with minimal payload to check auth
    payload = {
        'images': [],  # Empty for auth test
        'similar_images': False
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code in [200, 201]:
            print("✅ KindWise API key is VALID!")
        elif response.status_code == 400:
            # Bad request is expected with empty images, but means auth worked
            print("✅ KindWise API key is VALID! (400 expected with empty images)")
        else:
            print(f"❌ KindWise API key FAILED!")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ KindWise test FAILED: {e}")

def main():
    print("=" * 60)
    print("🔐 API AUTHENTICATION DEBUG TOOL")
    print("=" * 60)
    
    # Test OpenRouter API keys found in your code
    openrouter_keys = {
        "test_api_key.py": "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",
        "main_fastapi.py": "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",
        ".env file": "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"
    }
    
    for key_name, api_key in openrouter_keys.items():
        test_openrouter_api(api_key, key_name)
    
    # Test Telegram Bot
    telegram_token = "7565138619:AAH2XJA-iXvE_q4nEhltGyn6tBYLYV383xw"
    test_telegram_bot(telegram_token)
    
    # Test KindWise API
    kindwise_key = "u12lFbhGXOPacNJgi4pqK2scNsm34OryIiw99IIPJLKzjgntD5"
    test_kindwise_api(kindwise_key)
    
    print("\n" + "=" * 60)
    print("🔍 DEBUG COMPLETE")
    print("=" * 60)
    print("\n💡 Common solutions for 401 errors:")
    print("1. Check if API keys are expired or invalid")
    print("2. Verify account has sufficient credits/quota")
    print("3. Check for rate limiting")
    print("4. Ensure proper headers are included")
    print("5. Verify API endpoint URLs are correct")

if __name__ == "__main__":
    main()
