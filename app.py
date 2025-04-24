import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Census Visualizer", layout="wide")

st.title("📊 Census Profile Visualizer")
st.write("Upload your standardized Census Profile file to generate visualizations automatically.")

uploaded_file = st.file_uploader("Upload Census CSV", type=["csv", "tab"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, skiprows=3, encoding="ISO-8859-1")
        df.dropna(axis=1, how="all", inplace=True)
        df.columns = [col.strip().replace(" ", "_").lower() for col in df.columns]

        st.success("File parsed successfully!")

        # Example: Population growth chart
        pop_df = df[df["characteristic"].str.contains("Population, 20", na=False)]
        pop_df["total"] = pd.to_numeric(pop_df["total"], errors="coerce")

        fig, ax = plt.subplots()
        bars = ax.bar(pop_df["characteristic"], pop_df["total"], color=["gray", "blue"])
        ax.set_title("Population Growth (Census Years)")
        ax.bar_label(bars, fmt="%.0f")
        st.pyplot(fig)

        # By the Numbers box
        pop_vals = pop_df["total"].dropna().values
        if len(pop_vals) == 2:
            diff = int(pop_vals[1] - pop_vals[0])
            pct = (diff / pop_vals[0]) * 100
            st.info(f"**By the numbers:** Population increased by **{diff:,} people** ({pct:.1f}%) from 2016 to 2021.")

    except Exception as e:
        st.error(f"Failed to process file: {e}")
