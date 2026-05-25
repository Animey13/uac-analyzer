import re

with open('dashboard/app.py', 'r') as f:
    content = f.read()

# Make the tab names white
# The problem with tabs is streamlit's default styling overrides color
css_addition_2 = """
    /* Tab text color */
    .stTabs [data-baseweb="tab-list"] button {
        color: #f8fafc !important;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #3b82f6 !important;
        font-weight: bold;
    }
"""
content = content.replace("/* Global Backgrounds */", "/* Global Backgrounds */\n" + css_addition_2)

with open('dashboard/app.py', 'w') as f:
    f.write(content)
