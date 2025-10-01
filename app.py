import os
from groq import Groq
from dotenv import load_dotenv

# Load .env file
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

def ask_groq(question: str, model: str = "llama-3.1-8b-instant"):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant.Answer the following questions as best you can.DOnt make up answers."},
            {"role": "user", "content": question},  
        ],
        temperature=0.5,
        max_completion_tokens=512,
        top_p=1,
        stream=True,
    )

    full_answer = ""
    for chunk in completion:
        delta = chunk.choices[0].delta.content or ""
        print(delta, end="", flush=True)  
        full_answer += delta
    print()  
    return full_answer

def main():
    model = "llama-3.1-8b-instant"
    print(f"Using Groq model: {model}")

    try:
        while True:
            try:
                question = input("\nAsk anything (or type 'exit' to quit):\n> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye.")
                break

            if not question:
                continue
            if question.lower() in ("exit", "quit"):
                print("Goodbye.")
                break

            print("\n⏳ Asking Groq...\n")
            try:
                ask_groq(question, model=model)
            except Exception as e:
                print(f"ERROR: {e}")
                continue

    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")

if __name__ == "__main__":
    main()
