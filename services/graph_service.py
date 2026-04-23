from core.llm import generate_answer
import json
import re


class GraphService:

    def generate_graph(self, chunks):

        full_text = " ".join([c["text"] for c in chunks[:40]])

        if not full_text.strip():
            return {"nodes": [], "edges": []}

        prompt = f"""
You are an expert knowledge graph builder.

Extract a CLEAN and WELL-STRUCTURED knowledge graph.

Return ONLY JSON in this format:

{{
  "nodes": ["Concept1", "Concept2"],
  "edges": [
    {{"source": "Concept1", "target": "Concept2", "label": "relation"}}
  ]
}}

RULES:
- Maximum 25 nodes
- Maximum 35 edges
- Nodes must be SHORT
- No duplicates

Text:
{full_text}
"""

        response = generate_answer(prompt)

        # 🔥 أهم حماية
        if not response or not isinstance(response, str):
            return self.fallback_graph(chunks)

        data = self.clean_json(response)
        data = self.post_process(data)

        return data

    # ================= CLEAN JSON =================
    def clean_json(self, text):

        # 🔥 هذا السطر يحل المشكلة
        if not text or not isinstance(text, str):
            return {"nodes": [], "edges": []}

        try:
            return json.loads(text)

        except:
            match = re.search(r'\{.*\}', text, re.DOTALL)

            if match:
                try:
                    return json.loads(match.group())
                except:
                    pass

        return {"nodes": [], "edges": []}

    # ================= POST PROCESS =================
    def post_process(self, data):

        nodes = list(set(data.get("nodes", [])))

        clean_edges = []
        seen = set()

        for e in data.get("edges", []):

            src = e.get("source")
            tgt = e.get("target")
            label = e.get("label", "")

            if not src or not tgt:
                continue

            if src not in nodes or tgt not in nodes:
                continue

            key = (src, tgt, label)

            if key not in seen:
                clean_edges.append({
                    "source": src,
                    "target": tgt,
                    "label": label[:25]
                })
                seen.add(key)

        return {
            "nodes": nodes,
            "edges": clean_edges
        }
    

    def fallback_graph(self, chunks):

        nodes = []
        edges = []

        for i, c in enumerate(chunks[:10]):

            node_name = f"Node {i+1}"
            nodes.append(node_name)

            if i > 0:
                edges.append({
                    "source": nodes[i-1],
                    "target": node_name,
                    "label": "related"
                })

        return {
            "nodes": nodes,
            "edges": edges
        }