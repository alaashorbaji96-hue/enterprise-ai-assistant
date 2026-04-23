import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt


def render(df, numeric_cols, date_cols, cat_cols):

    st.markdown("## Relationships Analysis")

    # =========================
    # 🎨 STYLE
    # =========================
    color = st.color_picker("Theme Color", "#E6B800")

    heatmap_style = st.selectbox(
        "Heatmap Style",
        ["mako", "viridis", "rocket", "coolwarm"]
    )

    sns.set_theme(style="dark")

    plt.rcParams.update({
        "axes.facecolor": "#111111",
        "figure.facecolor": "#111111",
        "axes.labelcolor": "white",
        "xtick.color": "white",
        "ytick.color": "white",
        "text.color": "white",
    })

    if len(numeric_cols) < 2:
        st.warning("Not enough numeric columns")
        return

    corr = df[numeric_cols].corr()

    corr_pairs = (
        corr.unstack()
        .sort_values(ascending=False)
        .drop_duplicates()
    )

    filtered = corr_pairs[corr_pairs < 1]

    top5 = filtered.head(5)
    weak5 = filtered.tail(5)

    # ======================================================
    # 🔥 HEATMAP
    # ======================================================
    st.markdown("### Correlation Overview")

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.heatmap(
        corr,
        cmap=heatmap_style,
        annot=True,
        fmt=".2f",
        linewidths=0.5,
        linecolor="#222222",
        ax=ax
    )

    ax.set_title("Correlation Matrix", color="white")

    fig.patch.set_facecolor("#111111")
    ax.set_facecolor("#111111")

    st.pyplot(fig)

    # 🔘 BUTTON
    if st.button("Show Heatmap Insights"):

        st.markdown("#### Insights")

        for (c1, c2), val in top5.items():
            st.write(f"**{c1} ↔ {c2}** shows strong relationship ({round(val,2)})")

        for (c1, c2), val in weak5.items():
            st.write(f"**{c1} ↔ {c2}** shows weak relationship ({round(val,2)})")

    st.markdown("---")

    # ======================================================
    # 🔥 PAIRPLOT
    # ======================================================
    st.markdown("### Multi-Dimensional Relationships")

    subset_cols = numeric_cols[:4]

    pair_fig = sns.pairplot(
        df[subset_cols],
        corner=True,
        plot_kws={"color": color}
    )

    for ax in pair_fig.axes.flatten():
        if ax:
            ax.set_facecolor("#111111")

    pair_fig.fig.patch.set_facecolor("#111111")

    st.pyplot(pair_fig)

    # 🔘 BUTTON
    if st.button("Show Pair Insights"):

        st.markdown("#### Insights")

        for i in range(len(subset_cols)):
            for j in range(i + 1, len(subset_cols)):
                c1 = subset_cols[i]
                c2 = subset_cols[j]
                val = corr.loc[c1, c2]

                if val > 0.7:
                    st.write(f"**{c1} strongly relates to {c2}**")
                elif val > 0.3:
                    st.write(f"**{c1} moderately relates to {c2}**")
                else:
                    st.write(f"**{c1} weakly relates to {c2}**")

    st.markdown("---")

    # ======================================================
    # 🔥 TOP RELATIONSHIPS
    # ======================================================
    st.markdown("### Top Relationships")

    for (c1, c2), val in top5.items():

        fig, ax = plt.subplots(figsize=(5, 3))  # 👈 أصغر

        sns.regplot(
            x=df[c1],
            y=df[c2],
            scatter_kws={"color": color},
            line_kws={"color": "white"},
            ax=ax
        )

        ax.set_title(f"{c1} vs {c2}", color="white")
        ax.grid(alpha=0.2)

        fig.patch.set_facecolor("#111111")
        ax.set_facecolor("#111111")

        st.pyplot(fig)

        # 🔥 INSIGHT STYLE
        st.markdown(
            f"""
            <div style="
                font-size:16px;
                font-weight:600;
                color:#FFD700;
                margin-bottom:10px;">
                {c1} and {c2} have a strong relationship (correlation {round(val,2)})
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

    # ======================================================
    # 🔥 WEAK RELATIONSHIPS
    # ======================================================
    st.markdown("### Weak Relationships")

    weak3 = filtered.tail(3)

    for (c1, c2), val in weak3.items():

        fig, ax = plt.subplots(figsize=(5, 3))  # 👈 أصغر

        sns.scatterplot(
            x=df[c1],
            y=df[c2],
            color=color,
            ax=ax
        )

        ax.set_title(f"{c1} vs {c2}", color="white")
        ax.grid(alpha=0.2)

        fig.patch.set_facecolor("#111111")
        ax.set_facecolor("#111111")

        st.pyplot(fig)

        # 🔥 INSIGHT STYLE
        st.markdown(
            f"""
            <div style="
                font-size:16px;
                font-weight:600;
                color:#FF6B6B;
                margin-bottom:10px;">
                {c1} and {c2} show weak or no relationship (correlation {round(val,2)})
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")