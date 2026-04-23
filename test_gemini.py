import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-2.5-flash")

def generate_answer(context, question):
    prompt = f"""
    Answer the question based only on the context below.

    Context:
    {context}

    Question:
    {question}

    Answer clearly:
    """

    response = model.generate_content(prompt)

    return response.text