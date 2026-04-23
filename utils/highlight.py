import re

class Highlighter:
    @staticmethod
    def highlight_text(text, query):
        words = query.split()
        for word in words:
            if len(word) > 3:
                text = re.sub(
                    f"({word})",
                    r"<mark>\1</mark>",
                    text,
                    flags=re.IGNORECASE
                )
        return text