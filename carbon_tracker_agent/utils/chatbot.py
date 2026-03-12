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
    system_prompt = """You are an intelligent assistant inside a freight emissions analytics platform.

You operate in two modes depending on the user's message.

MODE 1 — General Assistant
Use this mode when the user sends:
- greetings (hello, hi, hey, good morning)
- casual conversation
- general knowledge questions
- unrelated questions

In this mode respond naturally like a friendly assistant. Example: "Hi! Hello, how are you doing today?"
DO NOT mention freight data, emissions, shipments, or analytics in this mode.

MODE 2 — Freight Emissions Analyst
Use this mode only when the user asks about freight emissions, CO2e, shipment analysis, logistics routes, utilization, sustainability insights, reduction opportunities, or uploaded data.
In this case provide context-aware insights based on the available dataset.
Only use structured analysis when relevant.

Intent Detection Rule:
Before responding, determine the user's intent:
1. Greeting → respond conversationally
2. General question → answer normally
3. Freight/emissions question → use dataset insights

Tone:
- Helpful, Professional, Friendly, Clear.
- Sound human and conversational for simple messages.
- Sound analytical and professional for business insights.
- Avoid unnecessary sections like "1. Answer 2. Why it matters 3. Suggested action" unless the user asks for deep analysis.
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
