import streamlit as st
from ivnse.core import fetch_fundamentals_yahoo, discounted_cash_flow
import math
import pandas as pd

st.title("Scenario Lab")
st.markdown("Run bull/base/bear scenarios for your stock.")

ticker = st.sidebar.text_input("NSE Ticker", value="INFY.NS", key="scenario_ticker")
base_growth = st.sidebar.number_input("Base Growth Rate (%)", 0.0, 30.0, 12.0, 1.0)
bull_multiplier = st.sidebar.slider("Bull Case Multiplier", 1.0, 2.0, 1.5, 0.1)
bear_multiplier = st.sidebar.slider("Bear Case Multiplier", 0.3, 1.0, 0.7, 0.1)
discount_rate = st.sidebar.slider("Discount Rate (%)", 6.0, 20.0, 12.0, 0.5) / 100
terminal_growth = st.sidebar.slider("Terminal Growth (%)", 0.0, 5.0, 2.0, 0.1) / 100

if not ticker:
    st.info("Enter a ticker to run scenario analysis.")
    st.stop()

cf_df, _, profile, _ = fetch_fundamentals_yahoo(ticker)
shares_out = profile.get("sharesOutstanding") or profile.get("marketCap", 0) / max(profile.get("previousClose", 1), 1)
if not shares_out:
    shares_out = 1e9
last_oe = 10000000000  # For demo, you can use calc_owner_earnings(cf_df) if you want real data

scenarios = [
    ("🐻 Bear", base_growth/100 * bear_multiplier),
    ("⚖️ Base", base_growth/100),
    ("🐂 Bull", base_growth/100 * bull_multiplier)
]

results = []
for name, g in scenarios:
    growth_rates = [g] * 3 + [g * 0.7] * 4 + [g * 0.5] * 3
    val = discounted_cash_flow(last_oe, growth_rates, discount_rate, terminal_growth, shares_out)
    results.append({"Scenario": name, "Fair Value": val})

df = pd.DataFrame(results)
st.bar_chart(df.set_index("Scenario")['Fair Value'])
