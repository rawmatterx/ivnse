import streamlit as st
from ivnse.ui_components.cards import glass_card, metric_card

glass_card("""
<h2>Welcome to ivnse 🚀</h2>
<p>This is your modern, multipage intrinsic value dashboard.<br>
Use the navigation bar to explore valuation, peers, scenarios, and reports.</p>
""")

metric_card("Sample KPI", "₹ 1,23,456", "+12.3%")
