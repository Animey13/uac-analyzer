import re

with open('dashboard/app.py', 'r') as f:
    content = f.read()

# 1. Fix Plotly YAxis titlefont to title_font
content = content.replace("titlefont=", "title_font=")

# 2. Fix the MoM table styling.
# Look for st.dataframe(disp_trends, use_container_width=True, hide_index=True)
# And replace with applying the color_mom format if possible.
# Actually, the arrows are applied via string manipulation, which makes it harder to use numeric styling.
# Wait, format_arrows makes it a string: "↑ 12.34%".
# The color_mom function expects a float. We can update color_mom to work with the arrow strings.
old_table = "st.dataframe(disp_trends, use_container_width=True, hide_index=True)"
new_table = """
            def style_arrows(val):
                if isinstance(val, str):
                    if val.startswith('↑'):
                        return 'color: #22c55e; font-weight: bold;'
                    elif val.startswith('↓'):
                        return 'color: #ef4444; font-weight: bold;'
                return ''

            st.dataframe(disp_trends.style.map(style_arrows), use_container_width=True, hide_index=True)
"""
content = content.replace(old_table, new_table)

# 3. Fix Sidebar dark mode styling
# Add this to the custom CSS block:
# .stSidebar, [data-testid="stSidebar"] { background-color: #0f172a !important; color: #f8fafc !important; }
# [data-testid="stSidebarContent"] { background-color: #0f172a !important; }

css_addition = """
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #1e293b !important;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] div, [data-testid="stSidebar"] span {
        color: #f8fafc;
    }
"""
content = content.replace("/* Hero Banner */", css_addition + "\n    /* Hero Banner */")

with open('dashboard/app.py', 'w') as f:
    f.write(content)
