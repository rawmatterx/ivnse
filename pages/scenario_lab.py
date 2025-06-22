import streamlit as st
import math
import yfinance as yf
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

tk = yf.Ticker(ticker)
info = tk.info
shares_out = info.get("sharesOutstanding") or info.get("marketCap", 0) / max(info.get("previousClose", 1), 1)
if not shares_out:
    shares_out = 1e9
last_price = info.get("previousClose") or math.nan

# Dummy owner earnings for demo
last_oe = 10000000000

def discounted_cash_flow(last_owner_earnings, growth_rates, discount_rate, terminal_growth, shares_outstanding):
    if math.isnan(last_owner_earnings) or last_owner_earnings <= 0:
        return math.nan
    flows = []
    oe = last_owner_earnings
    for g in growth_rates:
        oe *= (1 + g)
        flows.append(oe)
    terminal_value = flows[-1] * (1 + terminal_growth) / (discount_rate - terminal_growth)
    flows.append(terminal_value)
    pv = sum(f / (1 + discount_rate) ** (i + 1) for i, f in enumerate(flows))
    return pv / shares_outstanding if shares_outstanding else math.nan

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

cols = st.columns(3)
for i, row in df.iterrows():
    with cols[i]:
        st.metric(row['Scenario'], f"₹{row['Fair Value']:,.0f}")
