import streamlit as st
from utils.data_processor import DataProcessor


def render(df, numeric_cols, date_cols, cat_cols):

    st.markdown("## Overview")

    overview = DataProcessor.dataset_overview(df)

    # =========================
    # 🧠 SMART SUMMARY
    # =========================
    summary_text = f"""
    This dataset contains {overview['rows']:,} rows and {overview['columns']} columns.
    Missing values: {overview['missing_percent']}%.
    """
    st.info(summary_text)

    # =========================
    # 📊 KPIs
    # =========================
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rows", f"{overview['rows']:,}")
    col2.metric("Columns", overview["columns"])
    col3.metric("Missing", overview["missing"])
    col4.metric("Missing %", f"{overview['missing_percent']}%")

    st.markdown(" ")

    # =========================
    # 📌 DATA STATUS
    # =========================
    if overview["missing_percent"] == 0:
        st.success("High quality data — no missing values")
    elif overview["missing_percent"] < 5:
        st.success("Good quality data")
    elif overview["missing_percent"] < 20:
        st.warning("Moderate missing values — review recommended")
    else:
        st.error("High missing values — cleaning required")

    st.markdown("---")

    # =========================
    # 🧩 COLUMN STRUCTURE
    # =========================
    st.markdown("### Data Structure")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Numeric**")
        st.caption(f"{len(numeric_cols)} columns")

    with col2:
        st.markdown("**Date**")
        st.caption(f"{len(date_cols)} columns")

    with col3:
        st.markdown("**Categorical**")
        st.caption(f"{len(cat_cols)} columns")

    # =========================
    # 🧠 SMART HINT
    # =========================
    if len(numeric_cols) > 5:
        st.caption("Dataset contains many numeric features — correlation analysis recommended")

    st.markdown("---")

    # =========================
    # 📄 DATA PREVIEW (CLEAN UX)
    # =========================
    with st.expander("Preview Data"):

        view = st.radio(
            "Select view",
            ["First rows", "Random sample", "Last rows"],
            horizontal=True
        )

        if view == "First rows":
            st.dataframe(df.head(10))

        elif view == "Last rows":
            st.dataframe(df.tail(10))

        else:
            st.dataframe(df.sample(min(10, len(df))))

        st.caption("Showing a small sample for quick inspection")

    # =========================
    # 👉 NEXT STEP
    # =========================
    st.markdown("---")
    st.info("Go to Visualizations to explore patterns and trends")