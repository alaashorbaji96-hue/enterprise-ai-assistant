import os
import time
from dotenv import load_dotenv

load_dotenv()

# =========================================
# 🔑 API KEYS
# =========================================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# =========================================
# 🔵 GEMINI SETUP
# =========================================
import google.generativeai as genai

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel("models/gemini-2.5-flash")
else:
    gemini_model = None


# =========================================
# 🧠 LLM ROUTER
# =========================================
class LLMRouter:

    def __init__(self):
        self.cache = {}
        self.gemini_disabled = False

    # -------------------------------
    # 🧠 SMART ROUTING
    # -------------------------------
    def choose_model(self, prompt):
        if len(prompt) < 300:
            return "groq"
        return "gemini"

    # -------------------------------
    # 🚀 MAIN GENERATE
    # -------------------------------
    def generate(self, prompt):

        print("\n====== NEW REQUEST ======")

        if prompt in self.cache:
            print("Using cache")
            return self.cache[prompt]

        model_type = self.choose_model(prompt)
        print("Primary model:", model_type)

        try:
            if model_type == "groq":
                print("Trying GROQ...")
                answer = self.call_groq(prompt)
            else:
                print("Trying GEMINI...")
                answer = self.call_gemini(prompt)

            if not answer or not isinstance(answer, str):
                raise Exception("Empty response")

            self.cache[prompt] = answer
            return answer

        except Exception as e:
            print("❌ Primary failed:", e)

        # ============================
        # 🔵 GEMINI FALLBACK
        # ============================
        if not self.gemini_disabled and gemini_model:
            try:
                print("Trying GEMINI fallback...")
                answer = self.call_gemini(prompt)

                if not answer or not isinstance(answer, str):
                    raise Exception("Empty Gemini fallback")

                self.cache[prompt] = answer
                return answer

            except Exception as e:
                print("❌ Gemini failed:", e)

                if "quota" in str(e).lower() or "429" in str(e):
                    print("🚫 Gemini disabled بسبب quota")
                    self.gemini_disabled = True

        # ============================
        # 🟠 OPENROUTER
        # ============================
        try:
            print("Trying OPENROUTER...")
            answer = self.call_openrouter(prompt)

            if not answer or not isinstance(answer, str):
                raise Exception("Empty OpenRouter response")

            self.cache[prompt] = answer
            return answer

        except Exception as e:
            print("❌ OpenRouter failed:", e)

        # 🔥 آخر fallback
        return "⚠️ All models failed. Please try again."

    # -------------------------------
    # 🔥 STREAMING
    # -------------------------------
    def generate_stream(self, prompt):

        full_answer = self.generate(prompt)

        # 🔥 حماية قوية
        if full_answer is None:
            full_answer = ""

        if not isinstance(full_answer, str):
            full_answer = str(full_answer)

        if full_answer.strip() == "":
            full_answer = "⚠️ Failed to generate response. Please try again."

        words = full_answer.split(" ")

        current_text = ""

        for word in words:
            current_text += word + " "
            yield current_text
            time.sleep(0.02)

    # -------------------------------
    # 🟢 GROQ
    # -------------------------------
    def call_groq(self, prompt):
        from groq import Groq

        if not GROQ_API_KEY:
            raise Exception("Missing GROQ_API_KEY")

        client = Groq(api_key=GROQ_API_KEY)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.choices[0].message.content

        return content if content else "⚠️ Empty response from Groq"

    # -------------------------------
    # 🔵 GEMINI (FIXED 🔥)
    # -------------------------------
    def call_gemini(self, prompt):

        if not gemini_model:
            raise Exception("Gemini not configured")

        response = gemini_model.generate_content(prompt)

        # 🔥 FIX مهم جدًا
        if not response or not response.text:
            return "⚠️ Empty response from Gemini"

        return response.text

    # -------------------------------
    # 🟠 OPENROUTER
    # -------------------------------
    def call_openrouter(self, prompt):
        import requests

        if not OPENROUTER_API_KEY:
            raise Exception("Missing OPENROUTER_API_KEY")

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "meta-llama/llama-3-70b-instruct",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            },
            timeout=20
        )

        data = response.json()

        if "choices" in data:
            content = data["choices"][0]["message"]["content"]
            return content if content else "⚠️ Empty response from OpenRouter"

        raise Exception(f"OpenRouter error: {data}")


# =========================================
# 🎯 MAIN FUNCTION
# =========================================
router = LLMRouter()


def generate_answer(prompt, stream=False):

    if stream:
        return router.generate_stream(prompt)

    return router.generate(prompt)