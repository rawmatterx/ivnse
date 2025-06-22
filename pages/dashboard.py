import streamlit as st
import math
import yfinance as yf
import pandas as pd
from datetime import datetime
from ivnse.ui_components.cards import glass_card, metric_card

# --- Modern metric card ---
def create_metric_card(label: str, value: str, delta: str = None):
    delta_html = f'<div style="color:green;font-weight:600">{delta}</div>' if delta else ""
    return f"""
    <div style='background:rgba(255,255,255,0.15);backdrop-filter:blur(16px);border-radius:16px;padding:1.5rem;margin-bottom:1rem;text-align:center;'>
        <div style='font-size:2rem;font-weight:700;color:#6366f1'>{value}</div>
        <div style='color:#6b7280;font-size:0.9rem;font-weight:500;text-transform:uppercase;letter-spacing:0.05em'>{label}</div>
        {delta_html}
    </div>
    """

glass_card("""
<h2>Welcome to ivnse 🚀</h2>
<p>This is your modern, multipage intrinsic value dashboard.<br>
Use the navigation bar to explore valuation, peers, scenarios, and reports.</p>
""")

st.title("Dashboard")
st.markdown("Quick snapshot of your selected stock.")

ticker = st.sidebar.text_input("NSE Ticker", value="INFY.NS", key="dashboard_ticker")
if not ticker:
    st.info("Enter a ticker in the sidebar to see dashboard metrics.")
    st.stop()

tk = yf.Ticker(ticker)
info = tk.info
price = info.get("previousClose") or info.get("regularMarketPrice") or math.nan
market_cap = info.get("marketCap", 0)
pe = info.get("trailingPE", 0)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(create_metric_card("Price", f"₹{price:,.2f}" if price else "—"), unsafe_allow_html=True)
with col2:
    st.markdown(create_metric_card("Market Cap", f"₹{market_cap/1e9:,.1f}B" if market_cap else "—"), unsafe_allow_html=True)
with col3:
    st.markdown(create_metric_card("P/E Ratio", f"{pe:.2f}" if pe else "—"), unsafe_allow_html=True)

# Mini price chart
data = tk.history(period="6mo")
if not data.empty:
    st.line_chart(data["Close"], height=200)

st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
