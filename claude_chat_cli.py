import requests
import os
from dotenv import load_dotenv
load_dotenv()

print("\n🤖 Claude CLI Chat started. Type 'exit' to quit.\n")

API_KEY = os.getenv("ANTHROPIC_API_KEY")

print("\n🤖 Claude CLI Chat started. Type 'exit' to quit.\n")

def call_claude(user_message):
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    data = {
        "model": "claude-3-opus-20240229",
        "max_tokens": 1000,
        "messages": [
            {"role": "user", "content": user_message}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    if "content" in result and isinstance(result["content"], list):
        return result["content"][0]["text"]
    else:
        return "⚠️ Claude returned an unexpected response."

# ✅ Run interactive chat loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("👋 Exiting Claude CLI Chat. Goodbye!")
        break
    reply = call_claude(user_input)
    print("\nClaude: " + reply + "\n")
