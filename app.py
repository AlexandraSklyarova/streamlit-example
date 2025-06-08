# --- ECOFF Line ---
ecoff_line = alt.Chart(pd.DataFrame({"ECOFF": [ecoff_value]})).mark_rule(
    color='black',
    strokeDash=[5, 5]
).encode(
    x='ECOFF:Q'
)

# --- Resistance Threshold Line + Label ---
if antibiotic in resistance_cutoffs:
    res_val = resistance_cutoffs[antibiotic]

    # Red dashed line at resistance threshold
    red_line = alt.Chart(pd.DataFrame({"cutoff": [res_val]})).mark_rule(
        color='red',
        strokeDash=[5, 5]
    ).encode(
        x='cutoff:Q'
    )

    # Get middle bacterium name for label y-position
    middle_index = len(safe_df) // 2
    mid_bacterium = safe_df.sort_values(by=antibiotic, ascending=False).iloc[middle_index]["Bacteria"]

    # Label near the resistance threshold
    red_label = alt.Chart(pd.DataFrame({
        "cutoff": [res_val],
        "Bacteria": [mid_bacterium],
        "label": [f"{antibiotic} Resistance Cutoff = {res_val} μg/mL"]
    })).mark_text(
        align='left',
        dx=6,
        dy=0,
        fontSize=12,
        fontWeight='bold',
        color='red'
    ).encode(
        x='cutoff:Q',
        y=alt.Y('Bacteria:N'),
        text='label:N'
    )

    full_chart = bar_chart + red_line + red_label + ecoff_line

else:
    full_chart = bar_chart + ecoff_line
