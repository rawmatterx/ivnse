import streamlit as st
from ivnse.ui_components.nav import main_nav

# Apply global CSS (relative to repo root for Streamlit Cloud)
css_path = "ivnse/assets/ivnse.css"
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

main_nav()  # Top nav bar, sidebar, theme toggle

# Streamlit multipage navigation: use native pages (no custom router needed)
# Each page is a script in /pages/ and will be auto-discovered by Streamlit

def main():
    st.title("ivnse: Intrinsic Value Calculator")
    st.info("Use the sidebar to navigate between pages.")
    # Optionally, add a landing page or redirect to dashboard
