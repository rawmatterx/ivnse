import streamlit as st
from ui_components.nav import main_nav

# Apply global CSS
with open("assets/ivnse.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

main_nav()  # Top nav bar, sidebar, theme toggle

# Multipage routing
st.switch_page(
    {
        "Dashboard": "pages/dashboard.py",
        "Valuation": "pages/valuation.py",
        "Peer Comp": "pages/peers.py",
        "Scenario Lab": "pages/scenario_lab.py",
        "Reports": "pages/reports.py",
    }
)
