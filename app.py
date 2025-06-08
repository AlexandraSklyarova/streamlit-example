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

# Filter Sidebar
st.sidebar.title("Filters")
selected_gram = st.sidebar.multiselect("Select Gram Staining", options=df["Gram_Staining"].unique(), default=df["Gram_Staining"].unique())
selected_genus = st.sidebar.multiselect("Select Genus", options=df["Genus"].unique(), default=df["Genus"].unique())

filtered_df = df[df["Gram_Staining"].isin(selected_gram) & df["Genus"].isin(selected_genus)]

# Dropdown for Antibiotic
selected_antibiotic = st.selectbox("Select Antibiotic", ["Penicillin", "Streptomycin", "Neomycin"])

# Thresholds by Antibiotic
thresholds_dict = {
    "Penicillin": pd.DataFrame({
        "MIC": [8, 16, 32],
        "label": ["S", "I", "R"],
        "color": ["green", "orange", "red"]
    }),
    "Streptomycin": pd.DataFrame({
        "MIC": [32],
        "label": ["R"],
        "color": ["red"]
    }),
    "Neomycin": pd.DataFrame(columns=["MIC", "label", "color"])
}

# Prepare long-form data
long_df = filtered_df.melt(
    id_vars=["Bacteria", "Gram_Staining", "Genus"],
    value_vars=["Penicillin", "Streptomycin", "Neomycin"],
    var_name="Antibiotic",
    value_name="MIC"
)

# Filter for selected antibiotic
selected_df = long_df[long_df["Antibiotic"] == selected_antibiotic]

# Chart
bars = alt.Chart(selected_df).mark_bar().encode(
    x=alt.X("Bacteria:N", sort="-y", title="Bacteria"),
    y=alt.Y("MIC:Q", scale=alt.Scale(type="log"), title="MIC (µg/mL)"),
    color=alt.value("steelblue"),
    tooltip=["Bacteria", "Antibiotic", "MIC"]
).properties(width=800, height=400)

# Rules and Labels
thresholds = thresholds_dict[selected_antibiotic]
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

# Final chart
final_chart = (bars + rules + labels).configure_axisX(labelAngle=-45)
st.altair_chart(final_chart, use_container_width=True)
