import streamlit as st
import pandas as pd
import altair as alt

# --- Load the Data ---
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

# Filter based on user selection
st.sidebar.title("Filters")
selected_gram = st.sidebar.multiselect("Select Gram Staining", options=df["Gram_Staining"].unique(), default=df["Gram_Staining"].unique())
selected_genus = st.sidebar.multiselect("Select Genus", options=df["Genus"].unique(), default=df["Genus"].unique())

filtered_df = df[
    df["Gram_Staining"].isin(selected_gram) & df["Genus"].isin(selected_genus)
]


# ----- Streamlit Layout -----
# ----- Chart 1: Penicillin Resistance with Highlights -----
st.header("🔬 Penicillin Resistance")
st.markdown("""
**Story Insight:** Most bacteria are inhibited by small doses of Penicillin — but some, like *Aerobacter aerogenes*, are dramatically resistant.

We've added a label and highlight to emphasize this outlier.
""")

highlighted = filtered_df[filtered_df["Bacteria"] == "Aerobacter aerogenes"]

bars = alt.Chart(df_melted).mark_bar().encode(
    x=alt.X("Bacteria:N", sort="-y", title="Bacteria"),
    y=alt.Y("MIC:Q", scale=alt.Scale(type="log"), title="MIC (µg/mL)"),
    color="Antibiotic:N",
    tooltip=["Bacteria", "Antibiotic", "MIC"]
).properties(width=800, height=400)

# --- S/I/R thresholds for Penicillin ---
thresholds = pd.DataFrame({
    "MIC": [8, 16, 32],
    "label": ["S", "I", "R"],
    "color": ["green", "orange", "red"]
})

rules = alt.Chart(thresholds).mark_rule(strokeDash=[4, 4], size=2).encode(
    y="MIC:Q",
    color=alt.Color("color:N", scale=None)
)

labels = alt.Chart(thresholds).mark_text(
    align="left", baseline="bottom", dx=5, dy=-3, fontWeight="bold"
).encode(
    y="MIC:Q",
    text="label:N"
)

# --- Combine ---
final_chart = (bars + rules + labels).configure_axisX(labelAngle=-45)

# --- Display ---
st.altair_chart(final_chart, use_container_width=True)

# ----- Chart 3: MIC Comparison Across Antibiotics -----
st.header("📈 MIC Comparison Across Antibiotics")
st.markdown("""
**What does this show?**

Each line traces the Minimum Inhibitory Concentration (MIC) for one antibiotic across different bacteria.

- A **lower MIC** indicates higher effectiveness.
- Antibiotics behave differently depending on the organism. Streptomycin is effective against *Streptococcus hemolyticus*, but Penicillin is not.
""")

# Reshape data to long format
long_df = filtered_df.melt(
    id_vars=["Bacteria", "Gram_Staining", "Genus"],
    value_vars=["Penicillin", "Streptomycin", "Neomycin"],
    var_name="Antibiotic",
    value_name="MIC"
)

# Sort bacteria to match display
long_df["Bacteria"] = pd.Categorical(
    long_df["Bacteria"],
    categories=filtered_df.sort_values("Penicillin")["Bacteria"],
    ordered=True
)

# Create line chart
mic_lines = alt.Chart(long_df).mark_line(point=True).encode(
    x=alt.X("Bacteria:N", sort=None, title="Bacteria"),
    y=alt.Y("MIC:Q", scale=alt.Scale(type="log"), title="MIC (lower is more effective)"),
    color=alt.Color("Antibiotic:N", legend=alt.Legend(title="Antibiotic")),
    tooltip=["Bacteria", "Antibiotic", "MIC"]
).properties(
    width=700,
    height=400,
    title="MIC Trends Across Bacteria by Antibiotic"
).configure_axisX(labelAngle=-45)

st.altair_chart(mic_lines)

# ----- Chart 3: Antibiotic Heatmap -----
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

# ----- Ending Section -----
st.header("🧬 Final Thoughts")
st.markdown("""
This dataset reveals dramatic differences in bacterial resistance patterns.

- **Penicillin** has the highest variance in effectiveness — some bacteria are virtually immune.
- **Gram-positive bacteria** tend to be more sensitive overall.
- **Genus matters**: *Staphylococcus* species are extremely sensitive to Neomycin.

What other stories can you uncover? Try changing the filters above!
""")
