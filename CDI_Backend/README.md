# CDI Backend Configuration Guide

## Environment Variables Setup

The CDI Backend now uses environment variables for all configuration, making it more secure and flexible.

### 1. Quick Setup

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit the .env file:**
   ```bash
   # Edit with your favorite text editor
   notepad .env       # Windows
   nano .env          # Linux/Mac
   ```

3. **Add your API keys:**
   ```env
   KINDWISE_API_KEY=your_actual_kindwise_api_key_here
   OPENROUTER_API_KEY=your_actual_openrouter_api_key_here
   ```

### 2. Environment Variables Reference

#### Required Variables
- `KINDWISE_API_KEY` - Your KindWise API key for crop identification
- `OPENROUTER_API_KEY` - Your OpenRouter API key for AI treatment recommendations

#### Optional Variables (with defaults)
- `KINDWISE_API_URL` - KindWise API endpoint (default: https://crop.kindwise.com/api/v1/identification)
- `OPENROUTER_BASE_URL` - OpenRouter API base URL (default: https://openrouter.ai/api/v1)
- `OPENROUTER_MODEL` - AI model for treatments (default: deepseek/deepseek-chat)
- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 8000)
- `RELOAD` - Enable auto-reload (default: True)
- `LOG_LEVEL` - Logging level (default: info)
- `UPLOAD_DIR` - Upload directory (default: uploads)
- `MAX_IMAGE_SIZE` - Max image size in pixels (default: 1024)
- `JPEG_QUALITY` - JPEG compression quality (default: 95)

### 3. Starting the Backend

#### Option A: Use the startup script (Recommended)
```bash
# Windows
start_backend.bat

# Linux/Mac
chmod +x start_backend.sh
./start_backend.sh
```

#### Option B: Manual start
```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
python main_fastapi.py
```

### 4. Validation

Test your configuration:
```bash
python test_env.py
```

Or use the full validator:
```bash
python validate_config.py
```

### 5. API Endpoints

Once running, access:
- **Web Interface:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health
- **Configuration Info:** http://localhost:8000/api/info

### 6. Troubleshooting

#### Common Issues:

1. **Missing .env file:**
   ```
   Error: .env file not found!
   ```
   **Solution:** Copy `.env.example` to `.env` and configure it.

2. **Missing API keys:**
   ```
   WARNING: KINDWISE_API_KEY not found in environment variables!
   ```
   **Solution:** Add your actual API keys to the `.env` file.

3. **Permission denied (Linux/Mac):**
   ```
   Permission denied: ./start_backend.sh
   ```
   **Solution:** Make the script executable: `chmod +x start_backend.sh`

### 7. Security Notes

- ✅ **DO:** Keep your `.env` file local and never commit it to version control
- ✅ **DO:** Use different API keys for development and production
- ✅ **DO:** Regularly rotate your API keys
- ❌ **DON'T:** Share your `.env` file or API keys publicly
- ❌ **DON'T:** Hardcode API keys in your source code

### 8. Production Deployment

For production deployment, set environment variables directly on your server instead of using a `.env` file:

```bash
export KINDWISE_API_KEY="your_key_here"
export OPENROUTER_API_KEY="your_key_here"
export HOST="0.0.0.0"
export PORT="8000"
```

Or use your hosting platform's environment variable configuration (Heroku, DigitalOcean, AWS, etc.).

## File Structure

```
CDI_Backend/
├── .env                 # Your configuration (create from .env.example)
├── .env.example         # Example configuration file
├── main_fastapi.py      # Main FastAPI application
├── test.py             # Tkinter GUI application
├── requirements.txt     # Python dependencies
├── validate_config.py   # Configuration validator
├── test_env.py         # Simple environment test
├── start_backend.bat   # Windows startup script
├── start_backend.sh    # Linux/Mac startup script
└── uploads/            # Upload directory (auto-created)
```
