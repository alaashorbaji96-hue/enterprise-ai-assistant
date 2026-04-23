import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st

from app.views.home_page import HomePage
from app.views.upload_page import UploadPage
from app.views.dashboard_page import DashboardPage


# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Enterprise AI Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= SESSION INIT =================
if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"

if "demo" not in st.session_state:
    st.session_state.demo = False

# ================= GLOBAL STYLE =================
st.markdown("""
<style>

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0d0d0d;
    border-right: 1px solid #222;
    padding-top: 20px;
}

/* Main background */
[data-testid="stAppViewContainer"] {
    background: #0a0a0a;
}

/* Buttons */
button {
    border-radius:10px !important;
    height:45px !important;
    font-size:15px !important;
}

/* Remove top padding */
.block-container {
    padding-top: 1rem;
}

</style>
""", unsafe_allow_html=True)



# ================= SIDEBAR =================
with st.sidebar:

    st.markdown("""
    <div style="margin-bottom:20px;">
        <h2 style="margin-bottom:5px;">🧠 AI Platform</h2>
        <p style="color:#888;font-size:13px;">
        Document Intelligence System
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "🏠 Home"
        st.rerun()

    if st.button("📂 Upload", use_container_width=True):
        st.session_state.page = "📂 Upload"
        st.rerun()

    if st.button("📊 Dashboard", use_container_width=True):
        st.session_state.page = "📊 Dashboard"
        st.rerun()

    st.markdown("---")

    st.markdown("""
    <div style="color:#777;font-size:12px;margin-top:20px;">
    💀 AI Powered System<br>
    RAG + LLM + Graph
    </div>
    """, unsafe_allow_html=True)

# ================= ROUTING =================
if st.session_state.page == "🏠 Home":

    # ================= HERO =================
    st.markdown("""
    <div style="
    padding:40px;
    border-radius:20px;
    background: linear-gradient(135deg, #1f1f1f, #0a0a0a);
    border:1px solid #333;
    margin-bottom:30px;
    text-align:center;
    ">

    <h1 style="font-size:48px;margin-bottom:10px;">
    🧠 Enterprise AI Assistant
    </h1>

    <p style="color:#aaa;font-size:20px;">
    Transform Documents into Insights with AI
    </p>

    </div>
    """, unsafe_allow_html=True)

    # ================= STATS =================
    col1, col2, col3, col4 = st.columns(4)

    def stat_card(title, value):
        st.markdown(f"""
        <div style="
        background:#111;
        padding:20px;
        border-radius:12px;
        border:1px solid #333;
        text-align:center;
        ">
        <h3 style="color:#aaa">{title}</h3>
        <h1>{value}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col1:
        stat_card("Documents", "10K+")

    with col2:
        stat_card("Accuracy", "95%")

    with col3:
        stat_card("Speed", "Instant")

    with col4:
        stat_card("AI Models", "Multi")

    st.markdown("<br><br>", unsafe_allow_html=True)

    # ================= FEATURES =================
    st.markdown("### 🚀 Core Capabilities")

    col1, col2, col3 = st.columns(3)

    def feature_card(icon, title, desc):
        st.markdown(f"""
        <div style="
        background:#111;
        padding:20px;
        border-radius:15px;
        border:1px solid #333;
        height:180px;
        ">
        <h3>{icon} {title}</h3>
        <p style="color:#aaa;">
        {desc}
        </p>
        </div>
        """, unsafe_allow_html=True)

    with col1:
        feature_card("📄", "Smart Summaries",
                     "Generate structured summaries with key insights and explanations")

    with col2:
        feature_card("🌐", "Knowledge Graph",
                     "Visualize relationships between concepts and ideas")

    with col3:
        feature_card("💬", "AI Chat Assistant",
                     "Ask questions and get intelligent answers from documents")

    st.markdown("<br><br>", unsafe_allow_html=True)

    # ================= DEMO =================
    st.markdown("### 💀 Experience the Demo")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📂 Demo Upload Experience", use_container_width=True):
            st.session_state.page = "📂 Upload"
            st.session_state.demo = True
            st.rerun()

    with col2:
        if st.button("📊 Demo Dashboard Experience", use_container_width=True):
            st.session_state.page = "📊 Dashboard"
            st.session_state.demo = True
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ================= NORMAL FLOW =================
    st.markdown("### 📂 Or Upload Your Own Files")

    if st.button("Upload Files", use_container_width=True):
        st.session_state.page = "📂 Upload"
        st.session_state.demo = False
        st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)

    # ================= FOOTER =================
    st.markdown("""
    <div style="
    text-align:center;
    color:#666;
    font-size:12px;
    margin-top:30px;
    ">
    Built with AI • Streamlit • RAG • LLM
    </div>
    """, unsafe_allow_html=True)

    # Optional (إذا عندك محتوى إضافي)
    HomePage().render()


elif st.session_state.page == "📂 Upload":
    UploadPage().render()


elif st.session_state.page == "📊 Dashboard":

    if st.session_state.demo:
        st.info("🚀 Demo Dashboard Mode Activated")

    DashboardPage().render()