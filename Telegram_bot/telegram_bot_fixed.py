import os 
import json 
import requests 
from io import BytesIO 
from telegram import Update 
from telegram.ext import (
    ApplicationBuilder, 
    MessageHandler, 
    ContextTypes, 
    CommandHandler, 
    filters,
)
from openai import OpenAI

# ====== CONFIG ======

FASTAPI_BACKEND_URL = "http://localhost:8000/analyze"  # or your deployed URL
TEXT_AI_KEY = "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"
TEXT_AI_BASE = "https://openrouter.ai/api/v1"
TEXT_AI_MODEL = "deepseek/deepseek-chat"
BOT_TOKEN = "7565138619:AAH2XJA-iXvE_q4nEhltGyn6tBYLYV383xw"

# ====== MEMORY ======

user_memory = {}

# ====== TEXT AI CLIENT ======

text_ai = OpenAI(
    api_key=TEXT_AI_KEY, 
    base_url=TEXT_AI_BASE
)

# ====== HELPERS ======

def build_summary(result):
    crops = result.get("crops", [])
    diseases = result.get("diseases", [])
    summary = "\U0001f9ea Crop Analysis Result:\n"

    for crop in crops:
        summary += f"🌾 {crop['name']} ({crop['scientific_name']}), Confidence: {crop['confidence']}%\n"
    for disease in diseases:
        summary += f"⚠️ Disease: {disease['name']}, Confidence: {disease['confidence']}%\n"

    return summary.strip()

async def query_text_model(prompt):
    try:
        response = text_ai.chat.completions.create(
            model=TEXT_AI_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert agricultural assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error getting AI response: {str(e)}"

# ====== HANDLERS ======

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌿 Welcome to the Crop Disease Detector Bot!\nSend me a crop photo or ask a question.")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    caption = update.message.caption or ""

    # Download image from Telegram
    photo = update.message.photo[-1]
    file = await photo.get_file()
    image_bytes = await file.download_as_bytearray()

    # Send to FastAPI backend for analysis
    try:
        files = {'file': ('image.jpg', BytesIO(image_bytes), 'image/jpeg')}
        response = requests.post(FASTAPI_BACKEND_URL, files=files)
        response.raise_for_status()
        result = response.json()
    except Exception as e:
        await update.message.reply_text(f"❌ Error analyzing image: {e}")
        return

    # Build analysis summary
    summary = build_summary(result)
    user_memory[user_id] = {"last_summary": summary}

    # Build full prompt
    if caption:
        full_prompt = f"{summary}\n\nUser said: {caption}"
    else:
        full_prompt = summary

    # Query text model
    ai_response = await query_text_model(full_prompt)

    # Reply to user
    await update.message.reply_text(ai_response, parse_mode="Markdown")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message = update.message.text

    # Use memory if available
    memory = user_memory.get(user_id)
    if memory:
        prompt = f"{memory['last_summary']}\n\nUser asked: {message}"
    else:
        prompt = message

    ai_response = await query_text_model(prompt)
    await update.message.reply_text(ai_response, parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📷 Send a crop image.\n📝 Ask any plant health question.\n💡 I'll give you a smart diagnosis and treatment.")

# ====== MAIN ======

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
