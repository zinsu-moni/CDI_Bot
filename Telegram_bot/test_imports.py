print("Hello, Python is working!")
print("Testing imports...")
try:
    from telegram import Update
    from telegram.ext import ApplicationBuilder
    print("✅ Telegram imports successful")
except Exception as e:
    print(f"❌ Import error: {e}")

print("Test complete.")
