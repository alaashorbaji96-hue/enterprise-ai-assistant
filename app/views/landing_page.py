import streamlit as st


class LandingPage:

    def render(self):

        st.markdown("""
        <div style="
        text-align:center;
        margin-top:80px;
        ">

        <h1 style="font-size:48px;">🧠 AI Document Intelligence</h1>

        <p style="color:#aaa;font-size:18px;">
        Analyze, summarize, and explore documents using AI
        </p>

        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br><br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🚀 Try Demo", use_container_width=True):
                st.session_state.page = "upload"
                st.session_state.demo = True
                st.rerun()

        with col2:
            if st.button("📂 Upload Your File", use_container_width=True):
                st.session_state.page = "upload"
                st.rerun()

        st.markdown("<br><br>", unsafe_allow_html=True)

        # 💀 Feature Section
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("📄 **Smart Summaries**")

        with col2:
            st.markdown("🌐 **Knowledge Graphs**")

        with col3:
            st.markdown("💬 **AI Chat Assistant**")