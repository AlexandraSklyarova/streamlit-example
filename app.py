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
# ----- Chart 1: Penicillin Resistance with Highlights -----
st.header("🔬 Penicillin Resistance")
st.markdown("""
**Story Insight:** Most bacteria are inhibited by small doses of Penicillin — but some, like *Aerobacter aerogenes*, are dramatically resistant.

We've added a label and highlight to emphasize this outlier.
""")

highlighted = filtered_df[filtered_df["Bacteria"] == "Aerobacter aerogenes"]

base = alt.Chart(filtered_df).mark_bar().encode(
    x=alt.X("Penicillin:Q", title="MIC (Minimum Inhibitory Concentration)"),
    y=alt.Y("Bacteria:N", sort="-x"),
    color=alt.condition(
        alt.datum.Bacteria == "Aerobacter aerogenes",
        alt.value("crimson"),  # highlight
        alt.Color("Gram_Staining:N")
    ),
    tooltip=["Bacteria", "Penicillin", "Gram_Staining", "Genus"]
)

text = alt.Chart(highlighted).mark_text(
    align='left',
    baseline='middle',
    dx=5,
    fontSize=12,
    fontWeight='bold'
).encode(
    x="Penicillin:Q",
    y=alt.Y("Bacteria:N", sort="-x"),
    text=alt.value("🚨 Extremely Resistant")
)

rule = alt.Chart(pd.DataFrame({"x": [100]})).mark_rule(
    strokeDash=[4,4], color='black'
).encode(
    x="x:Q"
)

penicillin_story = (base + text + rule).properties(
    width=700,
    height=400,
    title="Penicillin Resistance (MIC) with Highlighted Outlier"
)

st.altair_chart(penicillin_story)


# ----- Chart 2: Streptomycin vs Neomycin -----
st.header("🧪 Streptomycin vs Neomycin Resistance")
st.markdown("Are there trade-offs in resistance between these two antibiotics?")

chart2 = alt.Chart(filtered_df).mark_circle(size=100).encode(
    x=alt.X("Streptomycin:Q", scale=alt.Scale(type='log'), title="Streptomycin MIC"),
    y=alt.Y("Neomycin:Q", scale=alt.Scale(type='log'), title="Neomycin MIC"),
    color="Genus:N",
    tooltip=["Bacteria", "Streptomycin", "Neomycin", "Gram_Staining"]
).properties(
    width=700,
    height=400
).interactive()

st.altair_chart(chart2)

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
