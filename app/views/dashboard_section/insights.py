import streamlit as st
from core.llm import generate_answer
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import os


def render(df, numeric_cols, date_cols, cat_cols):

    st.markdown("## AI Data Report")

    # =========================
    # 🧠 PROMPT
    # =========================
    summary = df.describe(include='all').to_string()

    prompt = f"""
You are a senior data analyst.

Create a professional structured report:

1. Executive Summary
2. Dataset Overview
3. Column Analysis
4. Statistical Summary
5. Relationships
6. Time Analysis (if exists)
7. Data Issues
8. Recommendations

Rules:
- Bullet points
- Clear insights
- No unnecessary text
- Business-focused

Data:
{summary}
"""

    # =========================
    # 🚀 GENERATE
    # =========================
    if st.button("Generate Full Report"):

        with st.spinner("Analyzing data..."):
            report = generate_answer(prompt)

        # =========================
        # 📊 CHARTS
        # =========================
        charts = []

        # 1. Histogram
        if numeric_cols:
            col = numeric_cols[0]
            fig, ax = plt.subplots()
            sns.histplot(df[col], kde=True, ax=ax)
            fig.savefig("hist.png")
            charts.append("hist.png")

        # 2. Boxplot
        if numeric_cols:
            fig, ax = plt.subplots()
            sns.boxplot(data=df[numeric_cols], ax=ax)
            fig.savefig("box.png")
            charts.append("box.png")

        # 3. Heatmap
        if len(numeric_cols) > 1:
            fig, ax = plt.subplots()
            corr = df[numeric_cols].corr()
            sns.heatmap(corr, cmap="mako", ax=ax)
            fig.savefig("heatmap.png")
            charts.append("heatmap.png")

        # 4. Time Trend
        if date_cols and numeric_cols:
            df_sorted = df.sort_values(date_cols[0])
            fig, ax = plt.subplots()
            ax.plot(df_sorted[date_cols[0]], df_sorted[numeric_cols[0]])
            fig.savefig("trend.png")
            charts.append("trend.png")

        # =========================
        # 🎨 DISPLAY
        # =========================
        st.markdown("### Report")

        st.markdown(
            f"""
            <div style="
                background:#111;
                padding:20px;
                border-radius:10px;
                color:white;
                line-height:1.8;
            ">
            {report}
            </div>
            """,
            unsafe_allow_html=True
        )

        for c in charts:
            st.image(c)

        # =========================
        # 📄 PDF
        # =========================
        def create_pdf(text, charts):

            doc = SimpleDocTemplate("report.pdf")
            styles = getSampleStyleSheet()
            content = []

            for line in text.split("\n"):
                content.append(Paragraph(line, styles["Normal"]))
                content.append(Spacer(1, 10))

            for img in charts:
                content.append(Image(img, width=400, height=250))
                content.append(Spacer(1, 20))

            doc.build(content)

        create_pdf(report, charts)

        with open("report.pdf", "rb") as f:
            st.download_button(
                "Download PDF Report",
                f,
                file_name="AI_Report.pdf"
            )

        # تنظيف الصور
        for c in charts:
            os.remove(c)