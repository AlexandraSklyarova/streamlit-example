with col1:
    img_chart = alt.Chart(filtered_df).mark_image(
        width=24,
        height=40
    ).encode(
        x=alt.X(f"{antibiotic}:Q", scale=alt.Scale(type='log', base=10), title="MIC (μg/mL, log scale)"),
        y=alt.Y("Bacteria:N", sort="-x"),
        url="icon:N",
        tooltip=["Bacteria", antibiotic, "Gram_Staining", "Genus"]
    ).properties(width=700, height=500)

    rule = alt.Chart(pd.DataFrame({"ECOFF": [ecoff_value]})).mark_rule(
        strokeDash=[5, 5], color='black'
    ).encode(
        x=alt.X("ECOFF:Q", scale=alt.Scale(type='log', base=10))
    )

    st.altair_chart(img_chart + rule)

with col2:
    st.markdown("""
    ### 🧪 How to Read This Chart

    - **Icons** represent each bacterium's MIC for the selected antibiotic.
    - The **x-axis is log-scaled** to reflect large differences in resistance.
    - The **dashed line** marks the ECOFF threshold at **1 μg/mL**:
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
