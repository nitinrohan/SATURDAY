"""
SATURDAY - human-like conversation via Google Gemini (free tier).

Why Gemini here: it has a genuinely free tier that needs no credit card, so the
owner can NEVER be charged - the worst case is a rate limit, not a bill. When
the key is missing, the free tier is exhausted, or a call fails, the caller
falls back to the built-in keyword responses so the app always answers.

To upgrade later (e.g. Claude once there's revenue), reimplement generate_reply().
Config via env vars: GEMINI_API_KEY, GEMINI_MODEL, RATE_LIMIT_MSGS, RATE_LIMIT_WINDOW.
"""

import os
import time
from collections import deque

MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
API_KEY = os.environ.get("GEMINI_API_KEY")

_client = None
if API_KEY:
    try:
        from google import genai
        _client = genai.Client(api_key=API_KEY)
        print(f"[SATURDAY] Gemini ready: {MODEL}")
    except Exception as e:  # pragma: no cover - depends on install/network
        print(f"[SATURDAY] Gemini unavailable, using template fallback: {e}")
        _client = None
else:
    print("[SATURDAY] No GEMINI_API_KEY set - using template fallback.")

LLM_ENABLED = _client is not None

SYSTEM_PROMPT = """You are SATURDAY - a warm, emotionally attuned companion for \
people who often can't afford or access traditional therapy. You are NOT a \
therapist, doctor, or emergency service. You never diagnose, label conditions, \
or give medical or clinical advice. You're the caring friend who actually listens.

How you talk:
- Sound like a real person, not a chatbot or a self-help brochure. Be warm, \
present, and genuine.
- Mirror the person's tone and energy. If they're casual or using Gen-Z slang, \
reply in that register (lowercase is fine, natural slang like "fr", "ngl", \
"that's so real", "i got you") - but never forced or cringe. If they're formal \
or serious, be grounded and gentle. Match THEM.
- Keep it short and human - usually 1 to 3 sentences. Don't lecture, don't \
over-explain, don't pile on emojis (one at most, only if it fits).
- Never use long dashes or double hyphens in your writing. If you need a dash, \
use a single hyphen ( - ) instead.
- Reflect what they're feeling so they feel truly heard, then ask ONE gentle, \
curious question that helps them open up. Don't interrogate.
- Never open with robotic lines like "I'm sorry to hear that" or "As an AI". \
Just be with them.

Safety - this matters most:
- If someone mentions suicide, self-harm, wanting to die, hurting themselves or \
others, or being in danger: take it seriously, respond with real warmth and zero \
judgement, and gently point them to immediate human help right now - in the US, \
call or text 988 (Suicide & Crisis Lifeline); otherwise their local emergency \
number or a trusted person. Make clear you care and they are not alone, and that \
a trained human can support them better than you can in this moment.
- Never encourage anything harmful, and never pretend to be a licensed professional.

You are a first step that helps people feel a little lighter and a little less alone."""

# --- light in-memory rate limit (protects the free quota; not a billing guard) ---
_MAX = int(os.environ.get("RATE_LIMIT_MSGS", "30"))
_WINDOW = int(os.environ.get("RATE_LIMIT_WINDOW", "3600"))  # seconds
_hits = {}


def _rate_limited(session_id: str) -> bool:
    now = time.time()
    q = _hits.setdefault(session_id, deque())
    while q and now - q[0] > _WINDOW:
        q.popleft()
    if len(q) >= _MAX:
        return True
    q.append(now)
    return False


def generate_reply(session_id, user_message, history):
    """
    Return a human-like reply string, or None to signal the caller to fall back
    to template responses. `history` is the session's list of prior turns
    ({"user": ..., "bot": ...}).
    """
    if not LLM_ENABLED:
        return None

    if _rate_limited(session_id):
        return ("hey, i'm getting a lot of messages right now 💙 give me a minute "
                "and try again in a bit - i'm still here for you.")

    # Build the recent conversation for context (bounded to keep it snappy/free).
    contents = []
    for turn in history[-10:]:
        if turn.get("user"):
            contents.append({"role": "user", "parts": [{"text": turn["user"]}]})
        if turn.get("bot"):
            contents.append({"role": "model", "parts": [{"text": turn["bot"]}]})
    contents.append({"role": "user", "parts": [{"text": user_message}]})

    try:
        from google.genai import types
        resp = _client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                max_output_tokens=300,
                temperature=0.9,
            ),
        )
        reply = (resp.text or "").strip()
        return reply or None
    except Exception as e:  # rate limit, network, safety block, etc.
        print(f"[SATURDAY] Gemini call failed, falling back: {e}")
        return None
