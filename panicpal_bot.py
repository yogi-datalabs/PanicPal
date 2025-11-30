import os
import ollama

# Load the persona prompt from the text file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PERSONA_PATH = os.path.join(BASE_DIR, "persona_prompt.txt")

with open(PERSONA_PATH, "r", encoding="utf-8") as f:
    PERSONA_PROMPT = f.read()


def chat_once(user_message: str) -> str:
    """
    Streams PanicPal's reply token-by-token using local llama3.1 via Ollama.
    Returns the full reply text (in case we want to log it later).
    """
    stream = ollama.chat(
        model="llama3.1",
        messages=[
            {"role": "system", "content": PERSONA_PROMPT},
            {"role": "user", "content": user_message},
        ],
        stream=True,
    )

    full_reply = ""

    for chunk in stream:
        token = chunk["message"]["content"]
        print(token, end="", flush=True)
        full_reply += token

    print()  # newline after full reply
    return full_reply


if __name__ == "__main__":
    print("PanicPal 🤍  (type 'quit' to exit)\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nPanicPal: Take care. I'm here whenever you need to talk again. 🤍")
            break

        if user_input.lower() in {"quit", "exit"}:
            print("\nPanicPal: Take care. I'm here whenever you need to talk again. 🤍")
            break

        print("\nPanicPal: ", end="", flush=True)
        reply = chat_once(user_input)

        print("\n" + "-" * 60 + "\n")
