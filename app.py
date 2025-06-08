import streamlit as st 
import pandas as pd 
import altair as alt 
import numpy as np

# ----- Data Setup ----- 
data = [
    {"Bacteria": "Aerobacter aerogenes", "Penicillin": 870, "Streptomycin": 1, "Neomycin": 1.6, "Gram_Staining": "negative", "Genus": "other"},
    {"Bacteria": "Bacillus anthracis", "Penicillin": 0.001, "Streptomycin": 0.01, "Neomycin": 0.007, "Gram_Staining": "positive", "Genus": "other"},
    {"Bacteria": "Brucella abortus", "Penicillin": 1, "Streptomycin": 2, "Neomycin": 0.02, "Gram_Staining": "negative", "Genus": "other"},
    {"Bacteria": "Diplococcus pneumoniae", "Penicillin": 0.005, "Streptomycin": 11, "Neomycin": 10, "Gram_Staining": "positive", "Genus": "other"},
    {"Bacteria": "Escherichia coli", "Penicillin": 100, "Streptomycin": 0.4, "Neomycin": 0.1, "Gram_Staining": "negative", "Genus": "other"},
    {"Bacteria": "Klebsiella pneumoniae", "Penicillin": 850, "Streptomycin": 1.2, "Neomycin": 1, "Gram_Staining": "negative", "Genus": "other"},
    {"Bacteria": "Mycobacterium tuberculosis", "Penicillin": 800, "Streptomycin": 5, "Neomycin": 2, "Gram_Staining": "negative", "Genus": "other"},
    {"Bacteria": "Proteus vulgaris", "Penicillin": 3, "Streptomycin": 0.1, "Neomycin": 0.1, "Gram_Staining": "negative", "Genus": "other"},
    {"Bacteria": "Pseudomonas aeruginosa", "Penicillin": 850, "Streptomycin": 2, "Neomycin": 0.4, "Gram_Staining": "negative", "Genus": "other"},
    {"Bacteria": "Salmonella (Eberthella) typhosa", "Penicillin": 1, "Streptomycin": 0.4, "Neomycin": 0.008, "Gram_Staining": "negative", "Genus": "Salmonella"},
    {"Bacteria": "Salmonella schottmuelleri", "Penicillin": 10, "Streptomycin": 0.8, "Neomycin": 0.09, "Gram_Staining": "negative", "Genus": "Salmonella"},
    {"Bacteria": "Staphylococcus albus", "Penicillin": 0.007, "Streptomycin": 0.1, "Neomycin": 0.001, "Gram_Staining": "positive", "Genus": "Staphylococcus"},
    {"Bacteria": "Staphylococcus aureus", "Penicillin": 0.03, "Streptomycin": 0.03, "Neomycin": 0.001, "Gram_Staining": "positive", "Genus": "Staphylococcus"},
    {"Bacteria": "Streptococcus fecalis", "Penicillin": 1, "Streptomycin": 1, "Neomycin": 0.1, "Gram_Staining": "positive", "Genus": "Streptococcus"},
    {"Bacteria": "Streptococcus hemolyticus", "Penicillin": 0.001, "Streptomycin": 14, "Neomycin": 10, "Gram_Staining": "positive", "Genus": "Streptococcus"},
    {"Bacteria": "Streptococcus viridans", "Penicillin": 0.005, "Streptomycin": 10, "Neomycin": 40, "Gram_Staining": "positive", "Genus": "Streptococcus"}
]

df = pd.DataFrame(data)

# ----- Streamlit Layout ----- 
st.title("💊 Antibiotic Resistance Exploration")
st.markdown("""
This interactive tool allows you to explore the **resistance levels of different bacteria** to three antibiotics: **Penicillin, Streptomycin, and Neomycin**.
Use the controls below to filter and compare bacteria by their **Gram stain** and **genus**.
""")

# ----- Filters ----- 
gram_options = st.multiselect("Select Gram Staining Type", df["Gram_Staining"].unique(), default=df["Gram_Staining"].unique())
genus_options = st.multiselect("Select Bacterial Genus", df["Genus"].unique(), default=df["Genus"].unique())

filtered_df = df[df["Gram_Staining"].isin(gram_options) & df["Genus"].isin(genus_options)]

# ----- Antibiotic Dropdown ----- 
antibiotic = st.selectbox("Select Antibiotic to Display", ["Penicillin", "Streptomycin", "Neomycin"], index=0)

# ----- ECOFF ----- 
ecoff_value = 1

# ----- Chart: Bar with Emoji Overlay -----
st.header(f"🔬 {antibiotic} Resistance")

unit_size = 1

# Compute the number of emojis per row (cap at 10 for sanity)
filtered_df["emoji_count"] = np.floor(filtered_df[antibiotic] / unit_size).astype(int).clip(upper=10)
filtered_df["emoji_label"] = filtered_df["emoji_count"].apply(lambda x: "🦠" * max(x, 1))  # Always show at least one

col1, col2 = st.columns([4, 2])

with col1:
    base = alt.Chart(filtered_df).encode(
        x=alt.X(f"{antibiotic}:Q", scale=alt.Scale(type='log', base=10), title="MIC (μg/mL, log scale)"),
        y=alt.Y("Bacteria:N", sort="-x")
    )

    bars = base.mark_bar(color="teal").encode(
        tooltip=["Bacteria", antibiotic, "Gram_Staining", "Genus"]
    )

    emojis = base.mark_text(
    align='left',
    baseline='middle',
    dx=5,
    fontSize=15
).encode(
    text="emoji_label:N"
)


    rule = alt.Chart(pd.DataFrame({"ECOFF": [ecoff_value]})).mark_rule(
        strokeDash=[5, 5], color='black'
    ).encode(
        x=alt.X("ECOFF:Q", scale=alt.Scale(type='log', base=10))
    )

    st.altair_chart(bars + emojis + rule, use_container_width=True)

with col2:
    st.markdown(f"""
    ### 🧪 How to Read This Chart

    - **Bars** represent MIC values (resistance level) for the selected antibiotic.
    - The **🦠 emoji** helps visually mark each bacterium on the chart.
    - The **x-axis is log-scaled** to reflect wide resistance ranges.
    - The **dashed line** marks the ECOFF threshold at **{ecoff_value} μg/mL**:
        - Left = **susceptible**
        - Right = **resistant**
    """)

# ----- Heatmap -----
st.header("🔥 Resistance Heatmap")
st.markdown("See the antibiotic resistance profile across all bacteria.")

melted = pd.melt(filtered_df, id_vars=["Bacteria"], value_vars=["Penicillin", "Streptomycin", "Neomycin"],
                 var_name="Antibiotic", value_name="MIC")

heatmap = alt.Chart(melted).mark_rect().encode(
    x=alt.X("Antibiotic:N"),
    y=alt.Y("Bacteria:N", sort=alt.EncodingSortField("MIC", op="max", order="descending")),
    color=alt.Color("MIC:Q", scale=alt.Scale(scheme='redyellowgreen', reverse=True)),
    tooltip=["Bacteria", "Antibiotic", "MIC"]
).properties(
    width=500,
    height=500
)

st.altair_chart(heatmap)

# ----- Ending -----
st.header("🧬 Final Thoughts")
st.markdown("""
This dataset reveals dramatic differences in bacterial resistance patterns.

- **Penicillin** has the highest variance in effectiveness — some bacteria are virtually immune.
- **Gram-positive bacteria** tend to be more sensitive overall.
- **Genus matters**: *Staphylococcus* species are extremely sensitive to Neomycin.
""")
