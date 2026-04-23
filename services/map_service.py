from core.llm import generate_answer


class MapService:

    def generate_map(self, chunks):

        full_text = " ".join([c["text"] for c in chunks[:50]])

        if not full_text or not full_text.strip():
            return "⚠️ No content available"

        prompt = f"""
Create a structured document map.

Format:
- Main Topic
    - Subtopic
        - Key Idea

Rules:
- Clear hierarchy
- No empty output
- Well organized

Text:
{full_text}
"""

        response = generate_answer(prompt)

        # 🔥 أهم حماية
        if not response or not isinstance(response, str):
            return self.fallback_map(chunks)

        return response

    # =========================================
    # 🔥 FALLBACK (NEW 💀)
    # =========================================
    def fallback_map(self, chunks):

        # ناخد أول كم chunk ونبني outline بسيط
        lines = []

        for i, c in enumerate(chunks[:10]):
            text = c["text"][:80].strip().replace("\n", " ")

            lines.append(f"- Topic {i+1}\n    - {text}")

        return "\n".join(lines)