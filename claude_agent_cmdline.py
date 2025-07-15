import sys
import os
import anthropic
from dotenv import load_dotenv

load_dotenv()  # Load API key from .env file

def get_prompt_from_args():
    if '--file' in sys.argv:
        file_index = sys.argv.index('--file') + 1
        try:
            with open(sys.argv[file_index], 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"[❌ ERROR] Couldn't read file: {e}")
            sys.exit(1)
    elif len(sys.argv) > 1:
        return ' '.join(sys.argv[1:])
    else:
        print("[❌ ERROR] No prompt or file provided.")
        sys.exit(1)

def get_claude_response(prompt):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        client = anthropic.Anthropic(api_key=api_key)

        try:
            response = client.messages.create(
                model="claude-3-opus-latest",
                max_tokens=1000,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            return f"[❌ API ERROR] {e}"


if __name__ == '__main__':
    prompt = get_prompt_from_args()
    print("📨 Sending to Claude...\n")
    reply = get_claude_response(prompt)
    print("🤖 Claude's Response:\n")
    print(reply)
