#!/usr/bin/env python3
"""
Simple test to check if environment variables are working
"""

import os
import sys

# Add current directory to Python path
sys.path.append(os.path.dirname(__file__))

def simple_env_test():
    try:
        # Try to load dotenv if available
        try:
            from dotenv import load_dotenv
            load_dotenv()
            print("✅ python-dotenv loaded successfully")
        except ImportError:
            print("⚠️  python-dotenv not installed, using system environment variables only")
        
        print("\n🔍 Environment Variables Check:")
        print("-" * 40)
        
        # Check for .env file
        env_file = ".env"
        if os.path.exists(env_file):
            print(f"✅ .env file found: {os.path.abspath(env_file)}")
        else:
            print(f"❌ .env file not found: {os.path.abspath(env_file)}")
        
        # Check key environment variables
        kindwise_key = os.getenv("KINDWISE_API_KEY")
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        
        print(f"\nKINDWISE_API_KEY: {'✅ Set' if kindwise_key else '❌ Not set'}")
        if kindwise_key:
            print(f"  Value: {kindwise_key[:20]}...")
            
        print(f"OPENROUTER_API_KEY: {'✅ Set' if openrouter_key else '❌ Not set'}")
        if openrouter_key:
            print(f"  Value: {openrouter_key[:20]}...")
        
        # Test API endpoints
        api_url = os.getenv("KINDWISE_API_URL", "https://crop.kindwise.com/api/v1/identification")
        openrouter_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        
        print(f"\nAPI Endpoints:")
        print(f"  KindWise: {api_url}")
        print(f"  OpenRouter: {openrouter_url}")
        
        # Configuration status
        if kindwise_key and openrouter_key:
            print("\n✅ Configuration looks good! Both API keys are set.")
            return True
        else:
            print("\n❌ Configuration incomplete. Missing API keys.")
            return False
            
    except Exception as e:
        print(f"❌ Error checking configuration: {e}")
        return False

if __name__ == "__main__":
    print("CDI Backend Environment Test")
    print("=" * 40)
    
    success = simple_env_test()
    
    if success:
        print("\n🚀 Ready to run: python main_fastapi.py")
    else:
        print("\n🔧 Please check your .env file configuration")
