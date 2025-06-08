import streamlit as st
import pandas as pd
import altair as alt

# --- Data ---
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

# --- Sidebar filters ---
st.sidebar.title("Filters")
selected_gram = st.sidebar.multiselect(
    "Select Gram Staining:",
    options=df["Gram_Staining"].unique(),
    default=list(df["Gram_Staining"].unique())
)
selected_genus = st.sidebar.multiselect(
    "Select Genus:",
    options=df["Genus"].unique(),
    default=list(df["Genus"].unique())
)

filtered_df = df[
    df["Gram_Staining"].isin(selected_gram) & df["Genus"].isin(selected_genus)
]

# --- Antibiotic selection ---
st.sidebar.title("Antibiotic Chart Selection")
selected_antibiotic = st.sidebar.selectbox(
    "Choose Antibiotic:",
    options=["Penicillin", "Streptomycin", "Neomycin"]
)

# --- Melt data for chosen antibiotic ---
df_melted = filtered_df[["Bacteria", selected_antibiotic]].rename(
    columns={selected_antibiotic: "MIC"}
)

# Sort bacteria by MIC ascending for nicer x-axis ordering
df_melted = df_melted.sort_values("MIC", ascending=True)

# --- S/I/R thresholds per antibiotic ---
thresholds_map = {
    "Penicillin": {"S": 8, "I": 16, "R": 32},
    "Streptomycin": {"R": 32},  # No S/I defined, only resistance threshold
    "Neomycin": {}  # No clinical breakpoints
}

thresholds = thresholds_map.get(selected_antibiotic, {})

# --- Bar chart ---
bars = alt.Chart(df_melted).mark_bar().encode(
    x=alt.X("Bacteria:N", sort=list(df_melted["Bacteria"]), title="Bacteria"),
    y=alt.Y("MIC:Q", scale=alt.Scale(type="log"), title="MIC (µg/mL)"),
    color=alt.value("steelblue"),
    tooltip=["Bacteria", "MIC"]
).properties(
    width=800,
    height=400,
    title=f"{selected_antibiotic} MIC by Bacteria"
)

# --- Add S/I/R dashed lines and labels ---
rules = []
labels = []
color_map = {"S": "green", "I": "orange", "R": "red"}

for label, val in thresholds.items():
    rule = alt.Chart(pd.DataFrame({"y": [val]})).mark_rule(strokeDash=[6, 4], color=color_map[label], size=2).encode(
        y="y:Q"
    )
    text = alt.Chart(pd.DataFrame({"y": [val], "label": [label]})).mark_text(
        align="left", baseline="bottom", dx=5, dy=-5, fontWeight="bold", color=color_map[label]
    ).encode(
        y="y:Q",
        text="label:N"
    )
    rules.append(rule)
    labels.append(text)

final_chart = bars
if rules:
    for r in rules:
        final_chart += r
    for l in labels:
        final_chart += l

final_chart = final_chart.configure_axisX(labelAngle=-45)

# --- Display bar chart ---
st.header(f"🔬 MIC Values for {selected_antibiotic}")
st.altair_chart(final_chart, use_container_width=True)

# --- Summary Table ---
st.header("📋 MIC Interpretation Summary")

summary_data = pd.DataFrame({
    "Antibiotic": ["Penicillin", "Streptomycin", "Neomycin"],
    "Susceptible MIC": ["≤ 8 µg/mL", "Not defined clinically", "Not established"],
    "Intermediate MIC": ["16 µg/mL", "—", "—"],
    "Resistant MIC": ["≥ 32 µg/mL", "≥ 32 µg/mL (NARMS)", "—"],
    "Notes": [
        "Standard CDC/CLSI breakpoints",
        "No clinical breakpoints; resistance threshold for surveillance",
        "No CDC/CLSI reference for human MIC standards"
    ]
})

# Format as a simple table for Streamlit
st.dataframe(summary_data)

# --- Final notes ---
st.markdown("""
---
### 🧬 Final Thoughts

- MIC values show how sensitive bacteria are to antibiotics.
- Lower MIC means more effective inhibition.
- Use filters and antibiotic selector above to explore patterns.
""")
