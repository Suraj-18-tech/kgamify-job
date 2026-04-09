import os
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

# Load env
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-3-flash-preview"

SYSTEM_PROMPT = """
You are KGamify AI Assistant.

ONLY answer questions related to:
- Jobs and career guidance
- Resume / CV building
- Interview preparation
- Skill roadmaps
- KGamify platform features

If the question is unrelated, politely refuse.
Be concise, professional, and helpful.
"""

# In-memory session store
chat_sessions = {}

def get_chat(user_id: str):
    if user_id not in chat_sessions:
        model = genai.GenerativeModel(MODEL_NAME)
        chat_sessions[user_id] = model.start_chat(history=[])
    return chat_sessions[user_id]


def chat_with_gemini(user_id: str, message: str) -> str:
    try:
        chat = get_chat(user_id)

        full_prompt = f"{SYSTEM_PROMPT}\nUser: {message}"

        response = chat.send_message(full_prompt)

        reply = response.text.strip()

        # Save history
        save_chat_history(user_id, "user", message)
        save_chat_history(user_id, "ai", reply)

        return reply

    except Exception as e:
        print("Gemini error:", e)
        return "⚠️ AI service is temporarily unavailable. Please try again."


# -------- FILE BASED HISTORY --------
def save_chat_history(user_id, role, text):
    os.makedirs("chat_history", exist_ok=True)
    file_path = f"chat_history/{user_id}.txt"

    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} | {role}: {text}\n")


def get_chat_history(user_id):
    file_path = f"chat_history/{user_id}.txt"
    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        return f.readlines()