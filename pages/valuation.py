import streamlit as st
from ivnse.core import fetch_fundamentals_yahoo, calc_owner_earnings, discounted_cash_flow, dividend_discount_model, create_metric_card
import math

st.title("Valuation")
st.markdown("Enter a ticker in the sidebar to run a full DCF & DDM valuation.")

ticker = st.sidebar.text_input("NSE Ticker", value="INFY.NS")
discount_rate = st.sidebar.slider("Discount Rate (%)", 6.0, 20.0, 12.0, 0.5) / 100
terminal_growth = st.sidebar.slider("Terminal Growth (%)", 0.0, 5.0, 2.0, 0.1) / 100
base_growth = st.sidebar.number_input("Growth Years 1-3 (%)", 0.0, 30.0, 12.0, 1.0)
mid_growth = st.sidebar.number_input("Growth Years 4-7 (%)", 0.0, 20.0, 8.0, 1.0)
tail_growth = st.sidebar.number_input("Growth Years 8-10 (%)", 0.0, 10.0, 5.0, 1.0)
div_growth = st.sidebar.slider("Dividend Growth (%)", 0.0, 15.0, 8.0, 0.5) / 100
mos = st.sidebar.slider("Margin of Safety (%)", 0, 50, 20, 5)

if not ticker:
    st.info("Enter a ticker to begin.")
    st.stop()

cf_df, div_df, profile, income_df = fetch_fundamentals_yahoo(ticker)
shares_out = profile.get("sharesOutstanding") or profile.get("marketCap", 0) / max(profile.get("previousClose", 1), 1)
if not shares_out:
    shares_out = 1e9
last_price = profile.get("previousClose") or math.nan
owner_earnings_series = calc_owner_earnings(cf_df)
last_oe = owner_earnings_series.iloc[-1] if not owner_earnings_series.empty else math.nan
last_div = div_df["dividend"].iloc[-1] if not div_df.empty and "dividend" in div_df.columns else 0

growth_rates = [base_growth / 100] * 3 + [mid_growth / 100] * 4 + [tail_growth / 100] * 3
dcf_val = discounted_cash_flow(last_oe, growth_rates, discount_rate, terminal_growth, shares_out) if not math.isnan(last_oe) else math.nan
ddm_val = dividend_discount_model(last_div, div_growth, discount_rate)
if not math.isnan(dcf_val) and ddm_val > 0:
    fair = (dcf_val + ddm_val) / 2
elif not math.isnan(dcf_val):
    fair = dcf_val
elif ddm_val > 0:
    fair = ddm_val
else:
    fair = math.nan
target_price = fair * (1 - mos / 100) if not math.isnan(fair) else math.nan
upside = ((fair - last_price) / last_price * 100) if not math.isnan(fair) and not math.isnan(last_price) and last_price > 0 else math.nan

st.markdown("<h3>Valuation Results</h3>", unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown(create_metric_card("DCF Value", f"₹{dcf_val:,.0f}" if not math.isnan(dcf_val) else "—"), unsafe_allow_html=True)
with col2:
    st.markdown(create_metric_card("DDM Value", f"₹{ddm_val:,.0f}" if ddm_val > 0 else "—"), unsafe_allow_html=True)
with col3:
    st.markdown(create_metric_card("Fair Value", f"₹{fair:,.0f}" if not math.isnan(fair) else "—"), unsafe_allow_html=True)
with col4:
    st.markdown(create_metric_card("Target Price", f"₹{target_price:,.0f}" if not math.isnan(target_price) else "—"), unsafe_allow_html=True)
with col5:
    upside_text = f"{upside:+.1f}%" if not math.isnan(upside) else "—"
    st.markdown(create_metric_card("Upside", upside_text), unsafe_allow_html=True)
