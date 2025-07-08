"""wave_cli_chatbot.py
======================
Minimal command-line chatbot powered by the Wave Engine.
• Remembers conversation history across runs (JSON file)
• No external dependencies / GPUs required
Run:
    python wave_cli_chatbot.py
Type `exit` or `quit` to leave.
"""

import json
import os
import time
from pathlib import Path

from wave_interactive_chatbot import WaveInteractiveChatbot

MEMORY_PATH = Path("wave_chat_memory.json")


def load_memory():
    if MEMORY_PATH.exists():
        try:
            with MEMORY_PATH.open("r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            # Corrupt or empty file – start fresh
            return []
    return []


def save_memory(history):
    def _default(obj):
        """JSON serializer for objects not serializable by default"""
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        return str(obj)

    try:
        with MEMORY_PATH.open("w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2, default=_default)
    except Exception as e:
        print(f"[!] Failed to save memory: {e}")


def main():
    print("🌊  Wave Engine CLI Chatbot – Persistent Memory Demo")
    print("Type 'exit' or 'quit' to end the session.\n")

    bot = WaveInteractiveChatbot()
    session_id = bot.start_session("local_user")

    # Load previous conversation history, if any
    previous_history = load_memory()
    if previous_history:
        bot.conversation_history.extend(previous_history)
        print(f"[Memory] Loaded {len(previous_history)} past exchanges.\n")

    while True:
        try:
            user_input = input("You> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            break

        if user_input.lower() in {"exit", "quit"}:
            break

        if not user_input:
            continue

        response_data = bot.process_user_input(session_id, user_input)
        print(f"Bot> {response_data['response_text']}\n")

        # Persist memory
        save_memory(list(bot.conversation_history))

    # Save on clean exit as well
    save_memory(list(bot.conversation_history))
    print("[Memory] Conversation saved. Bye!")


if __name__ == "__main__":
    main() 