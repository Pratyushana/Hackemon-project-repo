# Setting Up API Keys for GRACE Voice Agent

## Required Environment Variables

GRACE Voice Agent requires certain API keys to enable its full functionality. These should be stored in a `.env` file in the root directory of the project.

### Step 1: Create a `.env` file
Copy the `.env_template` file to a new file named `.env`:

```bash
cp .env_template .env
```

### Step 2: Add your API keys to the `.env` file

Open the `.env` file in a text editor and add your API keys:

```
# GRACE Voice Agent Environment Variables

# Google Gemini API Key (Required)
GEMINI_KEY=your_gemini_key_here

# OpenAI API Key (Optional)
OPENAI_KEY=your_openai_key_here

# Stability API Key (Optional)
STABILITY_KEY=your_stability_key_here

# HuggingFace Token (Optional)
HF_TOKEN=your_huggingface_token_here
```

### Required and Optional Keys

- **GEMINI_KEY**: Required for code analysis and AI features
- **OPENAI_KEY**: Optional, used for improved speech recognition via Whisper API
- **STABILITY_KEY**: Optional, used for image generation
- **HF_TOKEN**: Optional, alternative for image generation if Stability AI is unavailable

### Obtaining API Keys

1. **Google Gemini API Key**: 
   - Visit [Google AI Studio](https://ai.google.dev/)
   - Create an account or sign in
   - Generate an API key from the API section

2. **OpenAI API Key**:
   - Visit [OpenAI Platform](https://platform.openai.com/)
   - Create an account or sign in
   - Navigate to API keys and generate a new key

3. **Stability AI Key**:
   - Visit [Stability AI](https://stability.ai/)
   - Sign up for an account
   - Generate an API key from your dashboard

4. **Hugging Face Token**:
   - Visit [Hugging Face](https://huggingface.co/)
   - Create an account
   - Go to Settings → Access Tokens to create a token

## Security Notes

- Never share your API keys or commit them to public repositories
- The `.env` file is listed in `.gitignore` to prevent accidental commits
- If you need to share your configuration, use the `.env_template` file without actual keys 