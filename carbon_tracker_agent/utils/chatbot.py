import os
import time
import google.generativeai as genai
from .context_builder import build_context

# Model fallback chain — will try each in order if quota is exhausted
MODEL_FALLBACK_CHAIN = [
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-1.5-flash-latest",
    "gemini-1.5-pro-latest",
]

def initialize_gemini():
    from dotenv import load_dotenv
    load_dotenv(override=True)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("DEBUG: GEMINI_API_KEY not found in environment.")
        return None

    genai.configure(api_key=api_key)

    # Try each model in the fallback chain
    for model_name in MODEL_FALLBACK_CHAIN:
        try:
            model = genai.GenerativeModel(model_name)
            print(f"DEBUG: Initialized model: {model_name}")
            return model
        except Exception as e:
            print(f"DEBUG: Could not initialize {model_name}: {e}")

    print("DEBUG: All models failed to initialize.")
    return None


def _call_with_retry(model, prompt, max_retries=3, initial_wait=30):
    """
    Calls model.generate_content with exponential backoff on 429 quota errors.
    Returns (response_text, error_message).
    """
    wait = initial_wait
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response.text, None
        except Exception as e:
            err_str = str(e)
            # Check if it's a quota / rate-limit error
            if "429" in err_str or "quota" in err_str.lower() or "rate" in err_str.lower():
                # Check if daily quota is fully exhausted (no point retrying)
                if "GenerateRequestsPerDayPerProjectPerModel-FreeTier" in err_str:
                    return None, (
                        "⚠️ **Daily API quota exhausted.**\n\n"
                        "Your free-tier Gemini API key has hit its daily request limit. "
                        "Please try again tomorrow, or upgrade your Google AI Studio plan at "
                        "[ai.google.dev](https://ai.google.dev) to increase your quota."
                    )
                # Per-minute rate limit — wait and retry
                if attempt < max_retries - 1:
                    print(f"DEBUG: Rate limited (attempt {attempt+1}). Waiting {wait}s before retry...")
                    time.sleep(wait)
                    wait *= 2  # exponential backoff
                else:
                    return None, (
                        "⚠️ **Rate limit reached.** Too many requests in a short time.\n\n"
                        "Please wait a minute and try again. "
                        "If this persists, check your [Gemini API quota](https://ai.dev/rate-limit)."
                    )
            else:
                # Non-quota error — don't retry
                return None, f"⚠️ **AI Error:** {err_str}"

    return None, "⚠️ **Failed to get a response after multiple retries.** Please try again shortly."


def get_chat_response(model, messages, df, lane_df):
    system_prompt = """You are the Carbon Intelligence Agent, a highly capable AI assistant specialized in freight emissions analytics and sustainability optimization.

Your goal is to help users understand their carbon footprint and provide actionable insights for decarbonization.

You operate in two modes:

MODE 1 — Conversational Assistant
Use this mode for:
- Greetings and general help (e.g., "How can you help me?")
- Casual conversation
- Explaining your capabilities as an agent

In this mode, be friendly, proactive, and encouraging. Example: "👋 Hello! I'm your Carbon Intelligence Agent. I can analyze your shipment data, identify high-emission lanes, and suggest strategies to reduce your footprint. What would you like to explore first?"

MODE 2 — Freight Analytics Expert
Use this mode for:
- Deep analysis of emissions, CO2e, and routes.
- Sustainability strategy and truck technology comparisons.
- Insights based on the provided dataset.

Intent Detection Rule:
1. Always prioritize being helpful and proactive.
2. If the user asks about data or emissions, use the CONTEXT provided below to give precise, data-driven answers.
3. If the user asks a general question, answer as a knowledgeable logistics expert.

Tone:
- Proactive, Professional, Insightful, and Human-like.
- Use emojis sparingly but effectively (e.g., 🌱, 🚛, 📊) to maintain an engaging experience.
"""

    context = build_context(df, lane_df)

    # Build conversation history
    conversation = ""
    for msg in messages[:-1]:  # exclude the latest user message
        role = "User" if msg["role"] == "user" else "Assistant"
        conversation += f"{role}: {msg['content']}\n\n"

    latest_user_message = messages[-1]["content"]

    full_prompt = (
        f"{system_prompt}\n\n"
        f"=== CONTEXT (Use only for Mode 2) ===\n{context}\n\n"
        f"=== CONVERSATION HISTORY ===\n{conversation}\n"
        f"=== CURRENT MESSAGE ===\nUser: {latest_user_message}\nAssistant:"
    )

    response_text, error = _call_with_retry(model, full_prompt)
    if error:
        return error
    return response_text
