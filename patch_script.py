import re

with open('dashboard/app.py', 'r') as f:
    content = f.read()

# Streamlit markdown can sometimes parse HTML block incorrectly if there's blank lines.
# In the original, the hero banner string has blank lines.
# We'll use Streamlit's native `st.html()` or remove the blank lines inside the multiline f-string.
# Since st.html() was added in a later version of Streamlit, we will just format the HTML strictly.
html_block = """    st.markdown(f'''<div class="hero-container">
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

# replace the block
# Find the exact string from dashboard/app.py to replace
import textwrap

old_block = """    st.markdown(f\"\"\"
    <div class="hero-container">
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
    </div>
    \"\"\", unsafe_allow_html=True)"""

if old_block in content:
    content = content.replace(old_block, html_block)
else:
    print("Could not find old block to replace.")

with open('dashboard/app.py', 'w') as f:
    f.write(content)
