import streamlit as st
from ivnse.core import fetch_fundamentals_yahoo, create_metric_card
import pandas as pd

peer_groups = {
    "Technology": ["TCS.NS", "INFY.NS", "HCLTECH.NS", "WIPRO.NS"],
    "Banking": ["HDFCBANK.NS", "ICICIBANK.NS", "KOTAKBANK.NS", "AXISBANK.NS"],
    "Oil & Gas": ["RELIANCE.NS", "ONGC.NS", "IOC.NS", "BPCL.NS"],
    "Auto": ["MARUTI.NS", "TATAMOTORS.NS", "M&M.NS", "BAJAJ-AUTO.NS"]
}

st.title("Peer Comparison")
st.markdown("Compare valuation ratios with sector peers.")

sector = st.selectbox("Select Sector", list(peer_groups.keys()), key="peer_sector")
peers = peer_groups[sector]

peer_data = []
for peer in peers:
    _, _, profile, _ = fetch_fundamentals_yahoo(peer)
    pe = profile.get('trailingPE', 0)
    price = profile.get('previousClose', 0)
    market_cap = profile.get('marketCap', 0)
    peer_data.append({
        "Ticker": peer,
        "Price": price,
        "Market Cap (B)": market_cap/1e9 if market_cap else 0,
        "P/E Ratio": pe
    })

df = pd.DataFrame(peer_data)
st.dataframe(df, use_container_width=True)

# Bar chart for P/E comparison
st.bar_chart(df.set_index("Ticker")["P/E Ratio"])
