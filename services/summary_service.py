from core.llm import generate_answer
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from xml.sax.saxutils import escape
import io


class SummaryService:

    # ================= SUMMARY =================
    def generate_summary(self, chunks, summary_type, stream=False):

        full_text = " ".join([c["text"] for c in chunks[:50]])

        if summary_type == "Quick":
            prompt = f"""
Give a quick overview of this document.

- 5-7 bullet points
- Expand explanations where needed
- Do not be overly brief

Text:
{full_text}
"""

        elif summary_type == "Standard":
            prompt = f"""
Create a professional summary.

1. Executive Summary
2. Key Concepts
3. Key Points
4. Insight

- Expand explanations where needed
- Do not be overly brief

Text:
{full_text}
"""

        elif summary_type == "Detailed":
            prompt = f"""
Create an analytical summary.

Include:
- reasoning
- cause/effect
- insights
- real-world meaning
- graph ideas

- Expand explanations where needed
- Do not be overly brief

Text:
{full_text}
"""

        else:
            prompt = f"""
Turn this document into a full lesson.

Include:
- step-by-step explanation
- examples
- analogies
- mini recaps

- Expand explanations where needed
- Do not be overly brief

Text:
{full_text}
"""

        return generate_answer(prompt, stream=stream)

    # ================= PDF =================
    def generate_summary_pdf(self, summary):

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()

        # 🔥 Styles جديدة
        title_style = ParagraphStyle(
            "Title",
            parent=styles["Normal"],
            fontSize=14,
            leading=16,
            spaceAfter=10,
        )

        normal_style = styles["Normal"]

        content = []

        for line in summary.split("\n"):

            line = line.strip()

            if not line:
                continue

            safe_line = escape(line)

            # 🔥 Title (##)
            if line.startswith("##"):
                clean_line = safe_line.replace("##", "").strip()
                content.append(Paragraph(clean_line, title_style))

            # 🔥 Bullet (*)
            elif line.startswith("*"):
                content.append(Paragraph("• " + safe_line[1:].strip(), normal_style))

            # 🔥 Normal text
            else:
                content.append(Paragraph(safe_line, normal_style))

        doc.build(content)
        buffer.seek(0)

        return buffer