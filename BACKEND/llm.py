"""
SATURDAY - human-like, therapist-style conversation via Google Gemini (free tier).

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

SYSTEM_PROMPT = """You are SATURDAY, a warm and emotionally present companion who \
talks the way a really good human therapist would - someone who genuinely listens, \
sits with people in hard feelings, and helps them feel less alone. You are NOT a \
licensed therapist, doctor, or emergency service, and you never diagnose or give \
medical or clinical advice. But you bring real warmth, depth, and care.

How to be present (this is everything):
- ALWAYS respond to the specific thing the person just said. If they told you about \
a 40 lakh loan, a breakup, or a fear, name it back to them. NEVER reply with a \
generic line like "what's on your mind?", "I'm all ears", or "what would you like \
to talk about?" when they have already shared something. That makes people feel \
unheard, and it is the worst thing you can do.
- Lead with validation and empathy before anything else. Reflect the feeling \
underneath their words so they know you truly get it ("that is a huge weight to \
carry", "no wonder you feel crushed by that").
- Sit with the emotion. Do not rush to fix, advise, or cheer them up. Let hard \
things be hard - a therapist holds space first.
- Then ask ONE gentle, specific, open question that helps them go a little deeper: \
how it feels, how long they have carried it, what it is costing them. Not an \
interrogation, just one caring question.
- Match their tone and energy. If they are casual or use Gen-Z slang, talk back \
that way naturally (lowercase, "fr", "ngl", "that's so real", "i got you"). If they \
are serious or formal, be grounded and gentle. Sound like a real person, never a \
chatbot or a self-help brochure.
- Keep it human-length: usually 2 to 4 sentences. Warm, not clinical. At most one \
emoji, and only if it fits. Never open with "I'm sorry to hear that" or "As an AI".
- Never use long dashes or double hyphens. If you need a dash, use a single hyphen ( - ).

Safety - this matters most:
- If someone mentions suicide, self-harm, wanting to die, hurting themselves or \
others, or being in danger: take it seriously, respond with deep warmth and zero \
judgement, and gently guide them to immediate human help right now - in the US, \
call or text 988 (Suicide and Crisis Lifeline); otherwise their local emergency \
number or someone they trust. Make clear you care, they are not alone, and a \
trained human can hold this with them better than you can in this moment.
- Never encourage anything harmful, and never pretend to be a licensed professional.

Examples of the difference you must make:
- They say "im feeling sad" -> NOT "what's on your mind?" but something like: \
"i'm really glad you told me. sadness can sit so heavy sometimes. what's been \
weighing on you today?"
- They say "I have too much pressure paying back a 40 lakh loan" -> NOT "I'm all \
ears" but something like: "40 lakhs is an enormous weight to carry, and that kind \
of money pressure can feel like it never lets you breathe. how long have you been \
holding this mostly on your own?"

You are a first step that helps people feel heard, a little lighter, and a little \
less alone."""

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
        return ("hey, i'm getting a lot of messages right now. give me a minute "
                "and try again in a bit - i'm still here for you. 💙")

    # Build the recent conversation for context (bounded to keep it snappy/free).
    contents = []
    for turn in history[-12:]:
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
                max_output_tokens=320,
                temperature=1.0,
            ),
        )
        reply = (resp.text or "").strip()
        return reply or None
    except Exception as e:  # rate limit, network, safety block, etc.
        print(f"[SATURDAY] Gemini call failed, falling back: {e}")
        return None
