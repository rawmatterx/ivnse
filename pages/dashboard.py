import streamlit as st
from ivnse.core import fetch_fundamentals_yahoo, create_metric_card
import math

st.title("Dashboard")
st.markdown("Quick snapshot of your selected stock.")

ticker = st.sidebar.text_input("NSE Ticker", value="INFY.NS", key="dashboard_ticker")
if not ticker:
    st.info("Enter a ticker in the sidebar to see dashboard metrics.")
    st.stop()

cf_df, div_df, profile, income_df = fetch_fundamentals_yahoo(ticker)
price = profile.get("previousClose") or profile.get("regularMarketPrice") or math.nan
market_cap = profile.get("marketCap", 0)
pe = profile.get("trailingPE", 0)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(create_metric_card("Price", f"₹{price:,.2f}" if price else "—"), unsafe_allow_html=True)
with col2:
    st.markdown(create_metric_card("Market Cap", f"₹{market_cap/1e9:,.1f}B" if market_cap else "—"), unsafe_allow_html=True)
with col3:
    st.markdown(create_metric_card("P/E Ratio", f"{pe:.2f}" if pe else "—"), unsafe_allow_html=True)

# Mini price chart
try:
    import yfinance as yf
    tk = yf.Ticker(ticker)
    data = tk.history(period="6mo")
    if not data.empty:
        st.line_chart(data["Close"], height=200)
except Exception:
    pass

st.caption("Last updated: " + st.session_state.get('last_update', 'now'))
