import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Load API key
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")


client = Groq(api_key=api_key)
MODEL = "llama-3.1-8b-instant"

def ask_groq(question: str, model: str = MODEL) -> str:
  
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question},
        ],
        temperature=0.5,
        max_completion_tokens=512,
        top_p=1,
    )
    return completion.choices[0].message.content.strip()

# --- Streamlit UI ---
st.set_page_config(page_title="Groq Q&A Bot", page_icon="🤖")
st.title("🤖 Groq Q&A Bot")
st.write("Ask any question below and get instant answers powered by **Groq** models.")

# Input
question = st.text_area("Your Question:", placeholder="Type your question here...")

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question first.")
    else:
        with st.spinner("Thinking..."):
            try:
                answer = ask_groq(question)
                st.success("Answer:")
                st.write(answer)
            except Exception as e:
                st.error(f"Error: {e}")
