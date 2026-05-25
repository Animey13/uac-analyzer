import re

with open('dashboard/app.py', 'r') as f:
    content = f.read()

# Fix layout for KPI cards
# It looks like the cards wrapped because of whitespace or flexbox issues.
# We'll just replace the HTML with columns natively.
# Wait, native st.columns() doesn't allow custom background color on a per-column basis easily without st.markdown.
# Let's fix the HTML wrapper to use a single line.

html_block_2 = """    st.markdown(f'''<div class="hero-container"><div class="hero-title">UAC Care Transition & Placement Analytics</div><div class="hero-subtitle">Tracking how efficiently children move from CBP custody → HHS care → Sponsor placement</div><div style="display: flex; gap: 1rem; justify-content: space-between; margin-top: 2rem;"><div class="kpi-card" style="flex: 1;"><div class="kpi-value">{avg_te:.1f}%</div><div class="kpi-label">Transfer Efficiency</div><div class="kpi-indicator {te_color}"></div></div><div class="kpi-card" style="flex: 1;"><div class="kpi-value">{avg_de:.1f}%</div><div class="kpi-label">Discharge Effectiveness</div><div class="kpi-indicator {de_color}"></div></div><div class="kpi-card" style="flex: 1;"><div class="kpi-value">{avg_pt:.1f}%</div><div class="kpi-label">Pipeline Throughput</div><div class="kpi-indicator {pt_color}"></div></div><div class="kpi-card" style="flex: 1;"><div class="kpi-value">{int(total_anomalies)}</div><div class="kpi-label">Total Anomaly Days</div><div class="kpi-indicator {an_color}"></div></div></div></div>''', unsafe_allow_html=True)"""

old_block_2 = """    st.markdown(f'''<div class="hero-container">
        <div class="hero-title">UAC Care Transition & Placement Analytics</div>
        <div class="hero-subtitle">Tracking how efficiently children move from CBP custody → HHS care → Sponsor placement</div>
        <div style="display: flex; gap: 1rem; justify-content: center; margin-top: 2rem; flex-wrap: wrap;">
            <div class="kpi-card" style="flex: 1; min-width: 200px;">
                <div class="kpi-value">{avg_te:.1f}%</div>
                <div class="kpi-label">Transfer Efficiency</div>
                <div class="kpi-indicator {te_color}"></div>
            </div>
            <div class="kpi-card" style="flex: 1; min-width: 200px;">
                <div class="kpi-value">{avg_de:.1f}%</div>
                <div class="kpi-label">Discharge Effectiveness</div>
                <div class="kpi-indicator {de_color}"></div>
            </div>
            <div class="kpi-card" style="flex: 1; min-width: 200px;">
                <div class="kpi-value">{avg_pt:.1f}%</div>
                <div class="kpi-label">Pipeline Throughput</div>
                <div class="kpi-indicator {pt_color}"></div>
            </div>
            <div class="kpi-card" style="flex: 1; min-width: 200px;">
                <div class="kpi-value">{int(total_anomalies)}</div>
                <div class="kpi-label">Total Anomaly Days</div>
                <div class="kpi-indicator {an_color}"></div>
            </div>
        </div>
    </div>''', unsafe_allow_html=True)"""

if old_block_2 in content:
    content = content.replace(old_block_2, html_block_2)
else:
    print("Could not find old block to replace.")

with open('dashboard/app.py', 'w') as f:
    f.write(content)
