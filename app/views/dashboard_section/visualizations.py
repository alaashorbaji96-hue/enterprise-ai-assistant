import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt


def render(df, numeric_cols, date_cols, cat_cols):

    st.markdown("## Visual Analysis")

    # =========================
    # 🎨 COLOR CONTROL
    # =========================
    user_color = st.color_picker("Choose Theme Color", "#E6B800")

    # =========================
    # 🎨 GLOBAL STYLE
    # =========================
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
    # 🎯 SELECT COLUMN
    # =========================
    all_cols = numeric_cols + cat_cols

    if not all_cols:
        st.warning("No columns available")
        return

    selected_col = st.selectbox("Select Column", all_cols)
    is_numeric = selected_col in numeric_cols

    st.markdown(f"<h3 style='color:white'>{selected_col}</h3>", unsafe_allow_html=True)

    # =========================
    # 📊 NUMERIC DASHBOARD
    # =========================
    if is_numeric:

        # -------- Row 1 --------
        col1, col2 = st.columns(2)

        # Distribution
        with col1:
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.histplot(df[selected_col], kde=True, color=user_color, ax=ax)
            ax.set_title("Distribution", color="white")
            ax.grid(alpha=0.2)
            fig.patch.set_facecolor("#111111")
            ax.set_facecolor("#111111")
            st.pyplot(fig)

        # Boxplot
        with col2:
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.boxplot(x=df[selected_col], color=user_color, ax=ax)
            ax.set_title("Boxplot", color="white")
            ax.grid(alpha=0.2)
            fig.patch.set_facecolor("#111111")
            ax.set_facecolor("#111111")
            st.pyplot(fig)

        # -------- Row 2 --------
        col1, col2 = st.columns(2)

        # Violin
        with col1:
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.violinplot(x=df[selected_col], color=user_color, ax=ax)
            ax.set_title("Violin", color="white")
            ax.grid(alpha=0.2)
            fig.patch.set_facecolor("#111111")
            ax.set_facecolor("#111111")
            st.pyplot(fig)

        # Scatter
        if len(numeric_cols) > 1:
            other_col = [c for c in numeric_cols if c != selected_col][0]

            with col2:
                fig, ax = plt.subplots(figsize=(6, 4))
                sns.scatterplot(
                    x=df[selected_col],
                    y=df[other_col],
                    color=user_color,
                    ax=ax
                )
                ax.set_title(f"{selected_col} vs {other_col}", color="white")
                ax.grid(alpha=0.2)
                fig.patch.set_facecolor("#111111")
                ax.set_facecolor("#111111")
                st.pyplot(fig)

        # =========================
        # ⏳ TIME TREND (UPDATED)
        # =========================
        if date_cols:
            st.markdown("### Trend")

            date_col = date_cols[0]
            df_sorted = df.sort_values(date_col)

            fig, ax = plt.subplots(figsize=(10, 4))

            sns.lineplot(
                x=df_sorted[date_col],
                y=df_sorted[selected_col],
                color=user_color,
                ax=ax
            )

            # 🔥 تحسين القراءة
            ax.set_xticks(ax.get_xticks()[::5])
            plt.xticks(rotation=45)

            ax.tick_params(axis='x', labelsize=10, colors='white')
            ax.tick_params(axis='y', labelsize=10, colors='white')

            ax.grid(alpha=0.2)

            fig.patch.set_facecolor("#111111")
            ax.set_facecolor("#111111")

            st.pyplot(fig)

    # =========================
    # 🧩 CATEGORICAL DASHBOARD
    # =========================
    else:

        counts = df[selected_col].value_counts().head(10)

        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(
            x=counts.values,
            y=counts.index,
            color=user_color,
            ax=ax
        )

        ax.set_title("Top Categories", color="white")
        ax.grid(alpha=0.2)

        fig.patch.set_facecolor("#111111")
        ax.set_facecolor("#111111")

        st.pyplot(fig)