import streamlit as st
import pandas as pd
import altair as alt

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
st.title("💊 Antibiotic Resistance Explorer")

st.markdown("""
Explore how resistant various bacteria are to **Penicillin**, **Streptomycin**, and **Neomycin**.
You can filter by **Gram stain** and **bacterial genus**, and compare MIC values.
""")

# ----- Filters -----
gram_options = st.multiselect("Select Gram Staining Type", df["Gram_Staining"].unique(), default=df["Gram_Staining"].unique())
genus_options = st.multiselect("Select Bacterial Genus", df["Genus"].unique(), default=df["Genus"].unique())
filtered_df = df[df["Gram_Staining"].isin(gram_options) & df["Genus"].isin(genus_options)]

# ----- Antibiotic Selector -----
antibiotic = st.selectbox("Select Antibiotic to Display", ["Penicillin", "Streptomycin", "Neomycin"])

# ----- ECOFF Value -----
ecoff_value = 1

# ----- Bar Chart -----
st.header(f"🔬 {antibiotic} Resistance")

# Filter out non-positive values to avoid log scale issues
# Drop zero or negative MICs if any
# --- Zoomable Bar Chart with ECOFF line ---
safe_df = filtered_df[filtered_df[antibiotic] > 0]

bar_chart = alt.Chart(safe_df).mark_bar().encode(
    x=alt.X(f"{antibiotic}:Q", title="MIC (μg/mL, linear scale)"),
    y=alt.Y("Bacteria:N", sort='-x'),
    color=alt.Color("Gram_Staining:N", title="Gram Stain"),
    tooltip=["Bacteria", antibiotic, "Gram_Staining", "Genus"]
).properties(
    width=700,
    height=500
).interactive()

rule = alt.Chart(pd.DataFrame({"ECOFF": [ecoff_value]})).mark_rule(
    color='black',
    strokeDash=[5, 5]
).encode(
    x=alt.X("ECOFF:Q")
)

st.altair_chart(bar_chart + rule)

# --- Heatmap: Filtered by Selected Antibiotic ---
st.header("🔥 Resistance Heatmap")
st.markdown("See resistance levels for the selected antibiotic across all bacteria.")

melted = pd.melt(filtered_df,
                 id_vars=["Bacteria"],
                 value_vars=["Penicillin", "Streptomycin", "Neomycin"],
                 var_name="Antibiotic",
                 value_name="MIC")

melted = melted[melted["Antibiotic"] == antibiotic]

heatmap = alt.Chart(melted).mark_rect().encode(
    x=alt.X("Antibiotic:N"),
    y=alt.Y("Bacteria:N", sort=alt.EncodingSortField("MIC", op="max", order="descending")),
    color=alt.Color("MIC:Q", scale=alt.Scale(scheme='redyellowgreen', reverse=True)),
    tooltip=["Bacteria", "MIC"]
).properties(
    width=500,
    height=500
)

st.altair_chart(heatmap)


# ----- Most Effective Antibiotic Table -----
st.header("🏆 Most Effective Antibiotic by Bacterium")
st.markdown("This table shows the antibiotic with the **lowest MIC value** for each bacterium — the most effective one.")

# Find the most effective antibiotic (lowest MIC) for each row
mic_columns = ["Penicillin", "Streptomycin", "Neomycin"]
df_effective = filtered_df.copy()

# Find minimum MIC and corresponding antibiotic
df_effective["Most_Effective"] = df_effective[mic_columns].idxmin(axis=1)
df_effective["Lowest_MIC"] = df_effective[mic_columns].min(axis=1)

# Display results
st.dataframe(df_effective[["Bacteria", "Most_Effective", "Lowest_MIC"]].sort_values("Lowest_MIC"))


# ----- Ending -----
st.header("🧬 Final Thoughts")
st.markdown("""
- MIC (Minimum Inhibitory Concentration) values vary **dramatically** by antibiotic and bacterial species.
- A **log scale** helps us better visualize large differences.
- The **ECOFF** (epidemiological cutoff) helps distinguish wild type vs non-wild type behavior at 1 μg/mL.
""")
