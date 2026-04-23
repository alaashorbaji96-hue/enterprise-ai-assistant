import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# =========================
# 🔧 NORMALIZATION
# =========================
def normalize_data(series, method):
    if method == "Min-Max":
        return (series - series.min()) / (series.max() - series.min())
    elif method == "Z-score":
        return (series - series.mean()) / series.std()
    return series


# =========================
# 🚀 MAIN RENDER
# =========================
def render(df, numeric_cols, date_cols, cat_cols):

    st.markdown("## Data Explorer")

    # =========================
    # 🎨 STYLE
    # =========================
    color = st.color_picker("Theme Color", "#E6B800")

    sns.set_theme(style="dark")
    plt.rcParams.update({
        "axes.facecolor": "#111111",
        "figure.facecolor": "#111111",
        "axes.labelcolor": "white",
        "xtick.color": "white",
        "ytick.color": "white",
        "text.color": "white",
    })

    # =========================
    # 🌍 GLOBAL CONTROLS
    # =========================
    st.markdown("### Controls")

    sample_mode = st.selectbox("Sampling", ["Full Data", "Sample (1000 rows)"])

    if sample_mode == "Sample (1000 rows)" and len(df) > 1000:
        df = df.sample(1000)

    st.caption(f"Using {len(df)} rows")

    # =========================
    # 🧭 ANALYSIS TYPE
    # =========================
    analysis_type = st.selectbox(
        "Analysis Type",
        ["Univariate", "Bivariate", "Multivariate"]
    )

    # ======================================================
    # 🔷 UNIVARIATE
    # ======================================================
    if analysis_type == "Univariate":

        col = st.selectbox("Column", df.columns)

        chart_type = st.selectbox(
            "Chart",
            ["Histogram", "Boxplot", "Violin", "Bar"]
        )

        normalize = st.selectbox(
            "Normalize",
            ["None", "Min-Max", "Z-score"]
        )

        data = df[col]

        if col in numeric_cols:
            data = normalize_data(data, normalize)

        fig, ax = plt.subplots(figsize=(6, 4))

        if chart_type == "Histogram":
            sns.histplot(data, kde=True, color=color, ax=ax)

        elif chart_type == "Boxplot":
            sns.boxplot(x=data, color=color, ax=ax)

        elif chart_type == "Violin":
            sns.violinplot(x=data, color=color, ax=ax)

        else:
            counts = data.value_counts().head(10)
            sns.barplot(x=counts.values, y=counts.index, color=color, ax=ax)

        ax.set_facecolor("#111111")
        fig.patch.set_facecolor("#111111")

        st.pyplot(fig)

        # =========================
        # 🧠 INSIGHT
        # =========================
        if st.button("Explain"):

            st.markdown("### Insight Report")

            if col in numeric_cols:

                mean = data.mean()
                median = data.median()
                std = data.std()
                skew = data.skew()
                min_val = data.min()
                max_val = data.max()

                q1 = data.quantile(0.25)
                q3 = data.quantile(0.75)
                iqr = q3 - q1

                outliers = data[(data < q1 - 1.5 * iqr) | (data > q3 + 1.5 * iqr)]

                st.write(f"**{col} ranges from {round(min_val,2)} to {round(max_val,2)}.**")
                st.write(f"Mean = {round(mean,2)}, Median = {round(median,2)}.")

                if skew > 1:
                    st.write("Distribution is heavily right-skewed.")
                elif skew < -1:
                    st.write("Distribution is heavily left-skewed.")
                else:
                    st.write("Distribution is relatively balanced.")

                if len(outliers) > 0:
                    st.write(f"{len(outliers)} outliers detected.")
                else:
                    st.write("No significant outliers detected.")

                if std > mean:
                    st.write("High variability in values.")
                else:
                    st.write("Values are concentrated.")

            else:
                counts = data.value_counts(normalize=True)
                st.write(f"{col} contains {len(counts)} categories.")

                if counts.iloc[0] > 0.6:
                    st.write("Highly imbalanced distribution.")
                else:
                    st.write("Relatively balanced categories.")

    # ======================================================
    # 🔷 BIVARIATE
    # ======================================================
    elif analysis_type == "Bivariate":

        col1 = st.selectbox("X", df.columns)
        col2 = st.selectbox("Y", df.columns)

        chart_type = st.selectbox(
            "Chart",
            ["Scatter", "Regplot", "Boxplot", "Heatmap"]
        )

        normalize = st.selectbox(
            "Normalize",
            ["None", "Min-Max", "Z-score"]
        )

        fig, ax = plt.subplots(figsize=(6, 4))

        if chart_type == "Scatter":
            sns.scatterplot(
                x=normalize_data(df[col1], normalize),
                y=normalize_data(df[col2], normalize),
                color=color,
                ax=ax
            )

        elif chart_type == "Regplot":
            sns.regplot(
                x=df[col1],
                y=df[col2],
                scatter_kws={"color": color},
                line_kws={"color": "white"},
                ax=ax
            )

        elif chart_type == "Boxplot":
            sns.boxplot(x=df[col1], y=df[col2], color=color, ax=ax)

        else:
            heatmap_style = st.selectbox(
                "Heatmap Style",
                ["mako", "viridis", "rocket", "coolwarm"]
            )

            pivot = pd.crosstab(df[col1], df[col2])

            sns.heatmap(pivot, cmap=heatmap_style, ax=ax)

        ax.set_facecolor("#111111")
        fig.patch.set_facecolor("#111111")

        st.pyplot(fig)

        # =========================
        # 🧠 INSIGHT
        # =========================
        if st.button("Explain"):

            st.markdown("### Relationship Analysis")

            if col1 in numeric_cols and col2 in numeric_cols:

                corr = df[[col1, col2]].corr().iloc[0, 1]

                st.write(f"Correlation = {round(corr,2)}")

                if corr > 0.7:
                    st.write("Strong positive relationship.")
                elif corr < -0.7:
                    st.write("Strong negative relationship.")
                elif abs(corr) > 0.3:
                    st.write("Moderate relationship.")
                else:
                    st.write("Weak relationship.")

            else:
                st.write("Relationship depends on category distribution.")

    # ======================================================
    # 🔷 MULTIVARIATE
    # ======================================================
    else:

        selected = st.multiselect(
            "Columns",
            df.columns,
            default=df.columns[:3]
        )

        if len(selected) < 2:
            st.warning("Select at least 2 columns")
            return

        chart_type = st.selectbox(
            "Chart",
            ["Pairplot", "Scatter"]
        )

        if chart_type == "Pairplot":

            pair_fig = sns.pairplot(
                df[selected],
                corner=True,
                plot_kws={"color": color}
            )

            st.pyplot(pair_fig)

        else:

            fig, ax = plt.subplots(figsize=(6, 4))

            sns.scatterplot(
                x=df[selected[0]],
                y=df[selected[1]],
                hue=df[selected[2]] if len(selected) > 2 else None,
                ax=ax
            )

            st.pyplot(fig)

        # =========================
        # 🧠 INSIGHT
        # =========================
        if st.button("Explain"):

            st.markdown("### Multi-Variable Analysis")

            st.write(f"Analyzing {len(selected)} variables.")

            st.write("Look for clusters, patterns, and interactions.")

            st.write("Clusters indicate segmentation.")
            st.write("Linear patterns indicate strong relationships.")