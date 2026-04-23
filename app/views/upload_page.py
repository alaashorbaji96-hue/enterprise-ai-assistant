import streamlit as st
from services.document_service import DocumentService
from services.summary_service import SummaryService
from services.chat_service import ChatService
from services.map_service import MapService
from services.graph_service import GraphService
from utils.highlight import Highlighter
from streamlit_agraph import agraph, Node, Edge, Config
from utils.demo_data import get_demo_chunks

class UploadPage:

    def render(self):
        
        


        # ================= GLOBAL STYLE =================
        st.markdown("""
        <style>
        section[data-testid="stSidebar"] {
            background: #0d0d0d;
            border-right: 1px solid #222;
        }
        </style>
        """, unsafe_allow_html=True)

        # ================= TOP NAVBAR =================
        st.markdown("""
        <div style="
        display:flex;
        justify-content:space-between;
        align-items:center;
        padding:10px 0;
        margin-bottom:20px;
        border-bottom:1px solid #222;
        ">
        <div style="font-size:18px;">🧠 AI Platform</div>
        <div style="color:#aaa;">Prototype v1.0</div>
        </div>
        """, unsafe_allow_html=True)

        # ================= HERO =================
        st.markdown("""
        <div style="
        padding:25px;
        border-radius:15px;
        background: linear-gradient(135deg, #1f1f1f, #111);
        border:1px solid #333;
        margin-bottom:20px;
        ">
        <h1>🧠 Document Intelligence Platform</h1>
        <p style="color:#aaa;">
        Upload, analyze, and interact with your documents using AI
        </p>
        </div>
        """, unsafe_allow_html=True)

        # ================= FEATURE CARDS =================
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("📄 **Smart Summary**")

        with col2:
            st.markdown("🌐 **Knowledge Graph**")

        with col3:
            st.markdown("💬 **AI Chat Assistant**")

        st.markdown("---")

        # ================= EMPTY STATE =================
        if "chunks" not in st.session_state:

            st.markdown("""
            <div style="
            text-align:center;
            margin-top:60px;
            color:#aaa;
            ">
            <h3>📂 No documents uploaded yet</h3>
            <p>Upload your first PDF to start AI analysis</p>
            </div>
            """, unsafe_allow_html=True)

                # ================= DEMO MODE =================
        from utils.demo_data import get_demo_chunks

        if "demo" in st.session_state and st.session_state.demo:

            st.success("🚀 Demo Mode Activated")

            if "chunks" not in st.session_state:
                st.session_state.chunks = get_demo_chunks()
                st.session_state.index = None
                st.session_state.embeddings = None    

        # ================= UPLOAD BOX =================
        st.markdown("""
        <div style="
        background:#111;
        padding:15px;
        border-radius:10px;
        border:1px dashed #444;
        text-align:center;
        margin-bottom:15px;
        ">
        📂 Drop your PDF files here or click below
        </div>
        """, unsafe_allow_html=True)

        uploaded_files = st.file_uploader(
            "Upload PDF files", type="pdf", accept_multiple_files=True
        )

        if uploaded_files:
            with st.spinner("🧠 AI is analyzing your documents..."):
                self.process_files(uploaded_files)

        # ================= MAIN CONTENT =================
        if "chunks" in st.session_state:

            st.markdown("<br>", unsafe_allow_html=True)

            tab1, tab2, tab3, tab4 = st.tabs([
                "📄 Summary",
                "🧠 Map",
                "🌐 Graph",
                "💬 Chat"
            ])

            # ================= SUMMARY =================
            with tab1:

                st.markdown("""
                <div style="
                background:#111;
                padding:12px;
                border-radius:10px;
                border:1px solid #333;
                margin-bottom:10px;
                ">
                📄 AI Summary
                </div>
                """, unsafe_allow_html=True)

                summary_type = st.radio(
                    "Choose summary type:",
                    ["Quick", "Standard", "Detailed", "Full Explanation"]
                )

                if st.button("🚀 Generate Summary"):

                    service = SummaryService()
                    placeholder = st.empty()

                    stream = service.generate_summary(
                        st.session_state.chunks,
                        summary_type,
                        stream=True
                    )

                    full_text = ""

                    for chunk in stream:
                        full_text = chunk
                        placeholder.markdown(full_text)

                    st.session_state.summary = full_text
                    st.session_state.summary_type = summary_type

                if "summary" in st.session_state:
                    st.write(st.session_state.summary)

                    st.progress(0.9)
                    st.caption("AI Confidence: High")

                    service = SummaryService()
                    pdf = service.generate_summary_pdf(st.session_state.summary)

                    st.download_button(
                        "⬇️ Download Summary",
                        pdf,
                        file_name=f"{st.session_state.summary_type}.pdf"
                    )

            # ================= MAP =================
            with tab2:

                st.markdown("""
                <div style="
                background:#111;
                padding:12px;
                border-radius:10px;
                border:1px solid #333;
                margin-bottom:10px;
                ">
                🧠 Document Structure
                </div>
                """, unsafe_allow_html=True)

                if st.button("🧠 Generate Map"):
                    with st.spinner("Analyzing structure..."):
                        service = MapService()
                        st.session_state.doc_map = service.generate_map(
                            st.session_state.chunks
                        )

                if "doc_map" in st.session_state:
                    st.write(st.session_state.doc_map)

            # ================= GRAPH =================
            with tab3:

                st.markdown("""
                <div style="
                background:#111;
                padding:12px;
                border-radius:10px;
                border:1px solid #333;
                margin-bottom:10px;
                ">
                🌐 Knowledge Graph
                </div>
                """, unsafe_allow_html=True)

                if st.button("🌐 Generate Graph"):
                    with st.spinner("Building knowledge graph..."):
                        service = GraphService()
                        st.session_state.graph = service.generate_graph(
                            st.session_state.chunks
                        )

                        st.session_state.graph_key = 0

                if "graph" in st.session_state:

                    col1, col2 = st.columns([4, 1])

                    with col2:
                        if st.button("✨ Re-arrange"):
                            import copy
                            import random
                            new_graph = copy.deepcopy(st.session_state.graph)
                            random.shuffle(new_graph["nodes"])
                            st.session_state.graph = new_graph
                            st.rerun()

                    with col1:
                        self.render_graph(st.session_state.graph)

            # ================= CHAT =================
            with tab4:
                self.chat_ui()

    # ================= PROCESS FILES =================
    def process_files(self, uploaded_files):

        file_names = [f.name for f in uploaded_files]

        if "last_files" not in st.session_state or st.session_state.last_files != file_names:
            st.session_state.last_files = file_names
            st.session_state.processed = False

        if "processed" not in st.session_state or not st.session_state.processed:

            service = DocumentService()
            chunks, index, embeddings = service.process_files(uploaded_files)

            st.session_state.chunks = chunks
            st.session_state.index = index
            st.session_state.embeddings = embeddings
            st.session_state.processed = True

            st.success("PDFs processed successfully!")

    # ================= GRAPH =================
    def render_graph(self, graph):

        if not graph["nodes"]:
            st.warning("Graph generation failed")
            return

        nodes = [
            Node(
                id=n,
                label=n,
                shape="box",
                size=35,
                font={"size": 18},
                color="#00C853"
            )
            for n in graph["nodes"]
        ]

        edges = [
            Edge(
                source=e["source"],
                target=e["target"],
                label=e.get("label", ""),
                smooth=True
            )
            for e in graph["edges"]
        ]

        config = Config(
            width="100%",
            height=700,
            directed=True,
            physics=False,
            hierarchical=True,
        )

        agraph(nodes=nodes, edges=edges, config=config)

    # ================= CHAT =================
    def chat_ui(self):

        if "messages" not in st.session_state:
            st.session_state.messages = []

        query = st.chat_input("Ask your question...")

        if query:

            with st.chat_message("user"):
                st.write(query)

            st.session_state.messages.append({
                "role": "user",
                "content": query
            })

            service = ChatService()

            data = service.get_answer(
                query,
                st.session_state.chunks,
                st.session_state.index,
                st.session_state.embeddings
            )

            results = data["results"]
            count = data["count"]
            prompt = data["prompt"]
            answer_type = data["answer_type"]

            with st.chat_message("assistant"):
                st.markdown(f"### {answer_type}")

                placeholder = st.empty()
                stream = service.stream_answer(prompt)

                full_text = ""

                for chunk in stream:
                    full_text = chunk
                    placeholder.markdown(full_text)

                if count > 0:
                    with st.expander(f"📚 Sources ({count})"):
                        for r in results:
                            st.write(r["text"])