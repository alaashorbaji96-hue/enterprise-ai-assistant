import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from views.dashboard_section import overview
from views.dashboard_section import relationships
from views.dashboard_section import insights
from views.dashboard_section import explorer
from views.dashboard_section import visualizations
from core.llm import generate_answer
from utils.data_processor import DataProcessor
from utils.demo_data import get_demo_dataframe

class DashboardPage:

    def render(self):

        st.set_page_config(layout="wide")

        # ===================== HEADER =====================
        st.markdown("""
        # 🧠 AI Analytics Platform
        ### Intelligent Data Understanding & Insights Engine
        """)

        # ===================== STYLE =====================
        st.markdown("""
        <style>
            .stSelectbox label, .stRadio label {
                color: white !important;
                font-weight: 600;
            }
        </style>
        """, unsafe_allow_html=True)





        # ================= DEMO MODE =================
        if "demo" in st.session_state and st.session_state.demo:

            st.success("🚀 Demo Dashboard Mode")

            df = get_demo_dataframe()

        
            df = DataProcessor.clean_data(df)
            df = DataProcessor.handle_missing(df)

            numeric_cols, date_cols, cat_cols = DataProcessor.detect_types(df)

            # تشغيل dashboard مباشرة
            section = st.sidebar.radio(
                "📂 Navigate",
                ["Overview", "Visualizations", "Relationships", "Insights", "Explorer"]
            )

            if section == "Overview":
                overview.render(df, numeric_cols, date_cols, cat_cols)

            elif section == "Visualizations":
                visualizations.render(df, numeric_cols, date_cols, cat_cols)

            elif section == "Relationships":
                relationships.render(df, numeric_cols, date_cols, cat_cols)

            elif section == "Insights":
                insights.render(df, numeric_cols, date_cols, cat_cols)

            elif section == "Explorer":
                explorer.render(df, numeric_cols, date_cols, cat_cols)

            return

        # ===================== FILE UPLOAD =====================
        uploaded_file = st.file_uploader(
            "Upload CSV or Excel",
            type=["csv", "xlsx"]
        )

        if not uploaded_file:
            st.info("Upload a dataset to start analysis")
            return

        # ===================== LOAD DATA =====================
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        df = DataProcessor.clean_data(df)
        df = DataProcessor.handle_missing(df)

        numeric_cols, date_cols, cat_cols = DataProcessor.detect_types(df)

        # ===================== SIDEBAR =====================
        with st.sidebar:
            st.markdown("## 🧭 Navigation")

            section = st.radio(
                "",
                ["📊 Overview", "📈 Visualizations", "🔗 Relationships", "🧠 Insights", "🔍 Explorer"]
            )

        st.markdown("---")

        # ===================== OVERVIEW =====================
        if section == "📊 Overview":

            st.markdown("""
            <div style="
                background:#111;
                padding:15px;
                border-radius:10px;
                border:1px solid #333;
                margin-bottom:15px;
            ">
            <b>Dataset Overview & Quality Analysis</b>
            </div>
            """, unsafe_allow_html=True)

            overview.render(df, numeric_cols, date_cols, cat_cols)

        # ===================== VISUALIZATIONS =====================
        elif section == "📈 Visualizations":

            st.markdown("""
            <div style="
                background:#111;
                padding:15px;
                border-radius:10px;
                border:1px solid #333;
                margin-bottom:15px;
            ">
            <b>Visual Pattern Discovery & Distribution Analysis</b>
            </div>
            """, unsafe_allow_html=True)

            visualizations.render(df, numeric_cols, date_cols, cat_cols)

        # ===================== RELATIONSHIPS =====================
        elif section == "🔗 Relationships":

            st.markdown("""
            <div style="
                background:#111;
                padding:15px;
                border-radius:10px;
                border:1px solid #333;
                margin-bottom:15px;
            ">
            <b>Correlation & Feature Interaction Analysis</b>
            </div>
            """, unsafe_allow_html=True)

            relationships.render(df, numeric_cols, date_cols, cat_cols)

        # ===================== INSIGHTS =====================
        elif section == "🧠 Insights":

            st.markdown("""
            <div style="
                background:#111;
                padding:15px;
                border-radius:10px;
                border:1px solid #333;
                margin-bottom:15px;
            ">
            <b>AI-Generated Insights & Recommendations</b>
            </div>
            """, unsafe_allow_html=True)

            insights.render(df, numeric_cols, date_cols, cat_cols)

        # ===================== EXPLORER =====================
        elif section == "🔍 Explorer":

            st.markdown("""
            <div style="
                background:#111;
                padding:15px;
                border-radius:10px;
                border:1px solid #333;
                margin-bottom:15px;
            ">
            <b>Advanced Data Exploration & Deep Analysis</b>
            </div>
            """, unsafe_allow_html=True)

            explorer.render(df, numeric_cols, date_cols, cat_cols)