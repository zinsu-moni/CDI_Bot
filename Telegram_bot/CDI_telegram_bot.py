import os 
import json 
import requests 
import asyncio
from io import BytesIO 
from telegram import Update 
from telegram.ext import (
    ApplicationBuilder, 
    MessageHandler, 
    ContextTypes, 
    CommandHandler, 
    filters,
)
from telegram.error import TimedOut, NetworkError, BadRequest
from openai import OpenAI
from dotenv import load_doten
load_dotenv()

print("🔍 Debug: Environment variables loaded")
print(f"🔍 Debug: OPENROUTER_API_KEY = {os.getenv('OPENROUTER_API_KEY')}")
print(f"🔍 Debug: AI_SERVICE = {os.getenv('AI_SERVICE')}")

# ====== CONFIG ======

FASTAPI_BACKEND_URL = os.getenv("FASTAPI_BACKEND_URL", "http://localhost:8000/analyze")
AI_SERVICE = os.getenv("AI_SERVICE", "openrouter")

# OpenRouter Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE = "https://openrouter.ai/api/v1"
OPENROUTER_MODEL = "deepseek/deepseek-chat"

# OpenAI Configuration  
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE = "https://api.openai.com/v1"
OPENAI_MODEL = "gpt-3.5-turbo"

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7565138619:AAH2XJA-iXvE_q4nEhltGyn6tBYLYV383xw")

# ====== MEMORY ======

user_memory = {}

# ====== TEXT AI CLIENT ======

# Configure AI client based on chosen service
if AI_SERVICE == "openai":
    TEXT_AI_KEY = OPENAI_API_KEY
    TEXT_AI_BASE = OPENAI_BASE
    TEXT_AI_MODEL = OPENAI_MODEL
else:  # Default to OpenRouter
    TEXT_AI_KEY = OPENROUTER_API_KEY
    TEXT_AI_BASE = OPENROUTER_BASE
    TEXT_AI_MODEL = OPENROUTER_MODEL

print(f"🔍 Debug: Using AI service: {AI_SERVICE}")
print(f"🔍 Debug: TEXT_AI_KEY = {TEXT_AI_KEY}")
print(f"🔍 Debug: TEXT_AI_BASE = {TEXT_AI_BASE}")
print(f"🔍 Debug: TEXT_AI_MODEL = {TEXT_AI_MODEL}")

# Create OpenAI client with additional headers for OpenRouter
if AI_SERVICE == "openrouter":
    text_ai = OpenAI(
        api_key=TEXT_AI_KEY,
        base_url=TEXT_AI_BASE,
        default_headers={
            "HTTP-Referer": "https://github.com/your-repo",  # Optional
            "X-Title": "CDI Telegram Bot"  # Optional
        }
    )
else:
    text_ai = OpenAI(
        api_key=TEXT_AI_KEY, 
        base_url=TEXT_AI_BASE
    )

# ====== HELPERS ======

def build_summary(result):
    crops = result.get("crops", [])
    diseases = result.get("diseases", [])
    
    # Build a clean and readable summary
    summary = "CROP DISEASE ANALYSIS RESULTS\n" + "="*40 + "\n\n"
    
    if crops:
        summary += "IDENTIFIED CROPS:\n"
        for i, crop in enumerate(crops[:3], 1):  # Limit to top 3 for clarity
            confidence = crop.get('confidence', 0)
            name = crop.get('name', 'Unknown')
            scientific_name = crop.get('scientific_name', '')
            
            confidence_level = "HIGH" if confidence > 80 else "MEDIUM" if confidence > 60 else "LOW"
            summary += f"{i}. {name}"
            if scientific_name:
                summary += f" ({scientific_name})"
            summary += f" - {confidence}% confidence ({confidence_level})\n"
        summary += "\n"
    
    if diseases:
        summary += "DETECTED DISEASES/ISSUES:\n"
        for i, disease in enumerate(diseases[:3], 1):  # Limit to top 3
            confidence = disease.get('confidence', 0)
            name = disease.get('name', 'Unknown')
            
            severity_level = "HIGH" if confidence > 80 else "MEDIUM" if confidence > 60 else "LOW"
            summary += f"{i}. {name} - {confidence}% confidence ({severity_level} risk)\n"
        summary += "\n"
    
    if not crops and not diseases:
        summary += "No clear crop or disease identification found.\n"
        summary += "Please ensure the image shows:\n"
        summary += "- Clear view of the plant/crop\n"
        summary += "- Good lighting conditions\n"
        summary += "- Focus on affected areas if disease is suspected\n\n"
    
    # Add context for better AI analysis
    summary += "FOR DETAILED ANALYSIS:\n"
    summary += "Please provide additional information if available:\n"
    summary += "- Your location/climate zone\n"
    summary += "- Recent weather conditions\n"
    summary += "- When symptoms first appeared\n"
    summary += "- Any treatments already applied\n"
    
    return summary.strip()

async def query_text_model(prompt):
    try:
        # Check if API key is set
        if not TEXT_AI_KEY or TEXT_AI_KEY == "YOUR_NEW_OPENROUTER_API_KEY_HERE":
            return "⚠️ AI service not configured. Please set a valid API key in your .env file."
        
        print(f"🔍 Making API request with key: {TEXT_AI_KEY[:20]}...")
        print(f"🔍 Using base URL: {TEXT_AI_BASE}")
        print(f"🔍 Using model: {TEXT_AI_MODEL}")
        
        # Enhanced system prompt for better agricultural responses
        system_prompt = """You are an expert agricultural assistant and crop disease specialist. Your expertise includes:

- Crop disease identification and diagnosis
- Plant pathology and pest management  
- Agricultural best practices and farming techniques
- Organic and chemical treatment recommendations
- Prevention strategies for crop diseases
- Soil health and nutrient management
- Climate-specific farming advice

IMPORTANT GUIDELINES:
1. Always provide SPECIFIC, ACTIONABLE advice
2. Include both immediate treatment and long-term prevention
3. Mention specific products, chemicals, or organic solutions when relevant
4. Consider the crop type, disease severity, and growing conditions
5. Provide step-by-step treatment instructions
6. Include timing recommendations (when to apply treatments)
7. Suggest monitoring practices to track progress
8. Keep responses focused on agriculture - avoid unrelated topics
9. Use simple, clear language without excessive formatting characters

Format your responses clearly with:
DIAGNOSIS: What the problem is
TREATMENT: Immediate actions to take  
PREVENTION: How to avoid future issues
TIMELINE: When to apply treatments and expect results

Avoid using markdown formatting, emojis, or special characters. Keep it simple and readable."""

        response = text_ai.chat.completions.create(
            model=TEXT_AI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600,  # Increased for more detailed responses
            temperature=0.3  # Lower temperature for more focused responses
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        error_msg = str(e)
        print(f"🔍 Full error: {error_msg}")
        if "401" in error_msg or "auth" in error_msg.lower():
            service_name = "OpenAI" if AI_SERVICE == "openai" else "OpenRouter"
            return f"⚠️ {service_name} authentication failed. API Key: {TEXT_AI_KEY[:20]}... Error: {error_msg}"
        elif "rate limit" in error_msg.lower():
            return "⚠️ AI service rate limit exceeded. Please try again later."
        else:
            return f"⚠️ AI service error: {error_msg}"

# ====== HANDLERS ======

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = """Welcome to the Crop Disease Detection & Agricultural Assistant Bot!

What I can help you with:
- Disease Diagnosis - Send crop photos for disease identification
- Treatment Plans - Get specific treatment recommendations  
- Prevention Advice - Learn how to prevent crop diseases
- Agricultural Guidance - Ask any farming or crop-related questions

For best results when sending photos:
- Take clear, well-lit images of affected plants
- Focus on diseased areas or symptoms
- Include context about your location and growing conditions

Ask me questions like:
"How do I treat leaf blight in tomatoes?"
"What's the best fertilizer schedule for corn?"
"How can I prevent fungal infections?"

Ready to help improve your crop health!"""

    await update.message.reply_text(welcome_message)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    caption = update.message.caption or ""

    try:
        # Download image from Telegram with retry logic
        photo = update.message.photo[-1]
        await update.message.reply_text("📸 Processing your image...")
        
        # Retry logic for file download
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"Attempting to download file (attempt {attempt + 1}/{max_retries})")
                file = await photo.get_file()
                image_bytes = await file.download_as_bytearray()
                print(f"Successfully downloaded image: {len(image_bytes)} bytes")
                break
            except TimedOut:
                if attempt == max_retries - 1:
                    await update.message.reply_text("⏱️ Download timed out after multiple attempts. Please try sending a smaller image or try again later.")
                    return
                else:
                    print(f"Download attempt {attempt + 1} timed out, retrying...")
                    await asyncio.sleep(2)  # Wait before retry
            except NetworkError:
                if attempt == max_retries - 1:
                    await update.message.reply_text("🌐 Network error. Please check your connection and try again.")
                    return
                else:
                    print(f"Network error on attempt {attempt + 1}, retrying...")
                    await asyncio.sleep(2)

        # Send to FastAPI backend for analysis
        try:
            await update.message.reply_text("🔍 Analyzing your crop image...")
            files = {'file': ('image.jpg', BytesIO(image_bytes), 'image/jpeg')}
            response = requests.post(FASTAPI_BACKEND_URL, files=files, timeout=30)
            response.raise_for_status()
            result = response.json()
        except requests.exceptions.Timeout:
            await update.message.reply_text("⏱️ Analysis timed out. The backend service might be slow. Please try again.")
            return
        except requests.exceptions.ConnectionError:
            await update.message.reply_text("🔌 Cannot connect to analysis service. Please make sure the backend is running.")
            return
        except Exception as e:
            await update.message.reply_text(f"❌ Error analyzing image: {e}")
            return

        # Build analysis summary
        summary = build_summary(result)
        user_memory[user_id] = {"last_summary": summary}

        # Build enhanced prompt with more context
        context_prompt = f"""CROP DISEASE ANALYSIS REQUEST

{summary}

USER'S ADDITIONAL CONTEXT: {caption if caption else "No additional information provided"}

TASK: Based on the crop and disease identification results above, provide:

1. **IMMEDIATE DIAGNOSIS**: What is likely happening to this crop?
2. **TREATMENT PLAN**: Specific steps to treat the identified issues
3. **PREVENTION STRATEGY**: How to prevent this problem in the future
4. **MONITORING GUIDANCE**: What to watch for and when to take action

Please be specific with product names, application rates, and timing when possible. Focus on practical, actionable advice that a farmer can implement immediately."""

        # Query text model
        await update.message.reply_text("🤖 Getting expert agricultural analysis...")
        ai_response = await query_text_model(context_prompt)

        # Reply to user (removed markdown parsing to avoid formatting issues)
        await update.message.reply_text(ai_response)
        
    except Exception as e:
        await update.message.reply_text(f"❌ Unexpected error: {e}")
        print(f"Error in handle_photo: {e}")
        import traceback
        traceback.print_exc()

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message = update.message.text

    # Use memory if available for context-aware responses
    memory = user_memory.get(user_id)
    
    if memory:
        # User has previous crop analysis - provide contextual advice
        enhanced_prompt = f"""FOLLOW-UP AGRICULTURAL CONSULTATION

PREVIOUS CROP ANALYSIS:
{memory['last_summary']}

USER'S NEW QUESTION: {message}

TASK: Provide specific, expert agricultural advice that directly addresses the user's question while considering the previous crop analysis. Focus on:
- Practical solutions and treatments
- Product recommendations with application instructions
- Timeline for implementation and expected results
- Prevention strategies
- Monitoring and follow-up actions

Keep the response relevant to crop health and agriculture."""

        ai_response = await query_text_model(enhanced_prompt)
    else:
        # No previous analysis - general agricultural question
        general_prompt = f"""AGRICULTURAL CONSULTATION REQUEST

USER'S QUESTION: {message}

TASK: As an expert agricultural consultant, provide comprehensive advice on this farming/crop-related question. Include:
- Direct answer to the question
- Best practice recommendations
- Specific product or method suggestions when applicable
- Implementation timeline and steps
- What to monitor for success

Focus on practical, actionable advice that helps improve crop health and farming outcomes."""

        ai_response = await query_text_model(general_prompt)
    
    await update.message.reply_text(ai_response)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_message = """Crop Disease Detection Bot - Help Guide

Photo Analysis:
- Send clear crop/plant photos
- Include affected areas and symptoms
- Add context: location, weather, timing
- Get disease identification + treatment plans

Ask Questions About:
- Disease treatment and prevention
- Fertilizer and nutrient management  
- Pest control strategies
- Crop rotation and planning
- Soil health improvement
- Organic vs chemical solutions

Pro Tips:
- Mention your crop type and growth stage
- Include recent weather conditions
- Specify if you've tried any treatments
- Ask about timing for best results

Example Questions:
"My tomato leaves have brown spots, what should I do?"
"Best time to apply fungicide to wheat?"
"How to improve soil for corn planting?"

Follow-up: After photo analysis, ask specific questions for detailed guidance!"""

    await update.message.reply_text(help_message)

# ====== ERROR HANDLER ======

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Log the error and send a telegram message to notify the user."""
    print(f"Exception while handling an update: {context.error}")
    
    # Try to notify the user about the error
    if update and hasattr(update, 'effective_message') and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "🚫 Sorry, an error occurred while processing your request. Please try again."
            )
        except Exception:
            pass  # If we can't send a message, just ignore it

# ====== MAIN ======

def main():
    try:
        print("🔧 Initializing bot...")
        
        # Configure bot with longer timeouts
        app = (
            ApplicationBuilder()
            .token(BOT_TOKEN)
            .read_timeout(30)
            .write_timeout(30)
            .connect_timeout(30)
            .pool_timeout(30)
            .build()
        )
        print("✅ Bot application created successfully")

        # Add error handler
        app.add_error_handler(error_handler)
        
        # Add command and message handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
        print("✅ Handlers registered successfully")

        print("🤖 Bot is running...")
        print("🔗 Bot token:", BOT_TOKEN[:20] + "..." if len(BOT_TOKEN) > 20 else BOT_TOKEN)
        print(f"🤖 AI Service: {AI_SERVICE.upper()}")
        print("🔑 API key:", TEXT_AI_KEY[:20] + "..." if TEXT_AI_KEY and len(TEXT_AI_KEY) > 20 else "NOT SET")
        print("⏱️ Configured with 30s timeouts for better reliability")
        app.run_polling()
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Starting Telegram Bot...")
    print("📍 Current working directory:", os.getcwd())
    main()
