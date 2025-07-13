#!/usr/bin/env python3
"""
Configuration validator for CDI Backend
Checks if all required environment variables are properly set
"""

import os
from dotenv import load_dotenv

def validate_backend_config():
    """Validate CDI Backend configuration"""
    
    print("=" * 60)
    print("CDI BACKEND CONFIGURATION VALIDATOR")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    # Required environment variables
    required_vars = {
        "KINDWISE_API_KEY": "KindWise API key for crop identification",
        "OPENROUTER_API_KEY": "OpenRouter API key for AI treatment recommendations"
    }
    
    # Optional environment variables with defaults
    optional_vars = {
        "KINDWISE_API_URL": ("https://crop.kindwise.com/api/v1/identification", "KindWise API endpoint"),
        "OPENROUTER_BASE_URL": ("https://openrouter.ai/api/v1", "OpenRouter API base URL"),
        "OPENROUTER_MODEL": ("deepseek/deepseek-chat", "AI model for treatment recommendations"),
        "HOST": ("0.0.0.0", "FastAPI server host"),
        "PORT": ("8000", "FastAPI server port"),
        "RELOAD": ("True", "Enable auto-reload in development"),
        "LOG_LEVEL": ("info", "Logging level"),
        "UPLOAD_DIR": ("uploads", "Directory for uploaded files"),
        "MAX_IMAGE_SIZE": ("1024", "Maximum image size in pixels"),
        "JPEG_QUALITY": ("95", "JPEG compression quality")
    }
    
    all_good = True
    
    print("\n🔍 CHECKING REQUIRED VARIABLES:")
    print("-" * 40)
    
    for var_name, description in required_vars.items():
        value = os.getenv(var_name)
        if value:
            print(f"✅ {var_name}: {description}")
            print(f"   Value: {value[:20]}{'...' if len(value) > 20 else ''}")
        else:
            print(f"❌ {var_name}: {description}")
            print(f"   Status: NOT SET")
            all_good = False
        print()
    
    print("\n🔧 CHECKING OPTIONAL VARIABLES:")
    print("-" * 40)
    
    for var_name, (default_value, description) in optional_vars.items():
        value = os.getenv(var_name, default_value)
        print(f"✅ {var_name}: {description}")
        print(f"   Value: {value}")
        print()
    
    print("\n📋 CONFIGURATION SUMMARY:")
    print("-" * 40)
    
    if all_good:
        print("✅ All required environment variables are set!")
        print("✅ CDI Backend is properly configured!")
        print("\n🚀 Ready to start:")
        print("   python main_fastapi.py")
    else:
        print("❌ Some required environment variables are missing!")
        print("\n🔧 To fix this:")
        print("1. Copy .env.example to .env")
        print("2. Edit .env and add your actual API keys")
        print("3. Run this validator again")
    
    print("\n📁 Environment file locations:")
    env_file = os.path.join(os.getcwd(), ".env")
    example_file = os.path.join(os.getcwd(), ".env.example")
    
    if os.path.exists(env_file):
        print(f"✅ .env file found: {env_file}")
    else:
        print(f"❌ .env file missing: {env_file}")
    
    if os.path.exists(example_file):
        print(f"✅ .env.example found: {example_file}")
    else:
        print(f"⚠️  .env.example missing: {example_file}")
    
    return all_good

if __name__ == "__main__":
    success = validate_backend_config()
    
    if not success:
        print("\n" + "="*60)
        print("CONFIGURATION INCOMPLETE")
        print("="*60)
        exit(1)
    else:
        print("\n" + "="*60)
        print("CONFIGURATION VALID")
        print("="*60)
