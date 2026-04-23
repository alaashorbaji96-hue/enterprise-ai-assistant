from core.rag import search
from core.llm import generate_answer


class ChatService:

    def get_answer(self, query, chunks, index, embeddings):

        # ================= DEMO MODE (NO RAG) =================
        if index is None or embeddings is None:

            prompt = f"""
You are a professional AI assistant.

Answer clearly and professionally.

1. Explanation
2. Key Points
3. Insight
4. Simple Takeaway

Question:
{query}
"""

            return {
                "prompt": prompt,
                "results": [],
                "count": 0,
                "answer_type": "🚀 Demo Mode (General AI Answer)"
            }

        # ================= NORMAL RAG =================
        try:
            results, count = search(
                query,
                chunks,
                index,
                embeddings,
                k=8
            )
        except Exception:
            # 🔥 fallback إذا صار أي خطأ
            results, count = [], 0

        # ================= CONTEXT =================
        context = "\n\n".join([
            f"[File: {r.get('source', 'Unknown')} | Page: {r.get('page', '-')}]"
            f"\n{r.get('text', '')[:200]}"
            for r in results
        ])

        # ================= TYPE =================
        answer_type = "📄 Based on document" if count > 0 else "🌐 General knowledge"

        # ================= PROMPT =================
        prompt = f"""
You are a professional AI consultant.

1. Explanation
2. Key Points
3. Insights
4. Takeaway

Context:
{context}

Question:
{query}
"""

        return {
            "prompt": prompt,
            "results": results,
            "count": count,
            "answer_type": answer_type
        }

    # ================= STREAMING =================
    def stream_answer(self, prompt):

        # 🔥 حماية إضافية
        if not prompt:
            return iter(["⚠️ No prompt provided"])

        return generate_answer(prompt, stream=True)