import streamlit as st
import math
import os
import pandas as pd
import yfinance as yf
from datetime import date, datetime
from typing import Optional
from ivnse.ui_components.cards import glass_card

# --- Modern UI helpers (minimal for now) ---
def create_metric_card(label: str, value: str, delta: Optional[str] = None, delta_color: str = "normal"):
    delta_html = f'<div style="color:green;font-weight:600">{delta}</div>' if delta else ""
    return f"""
    <div style='background:rgba(255,255,255,0.15);backdrop-filter:blur(16px);border-radius:16px;padding:1.5rem;margin-bottom:1rem;text-align:center;'>
        <div style='font-size:2rem;font-weight:700;color:#6366f1'>{value}</div>
        <div style='color:#6b7280;font-size:0.9rem;font-weight:500;text-transform:uppercase;letter-spacing:0.05em'>{label}</div>
        {delta_html}
    </div>
    """

def fetch_fundamentals_yahoo(ticker: str):
    try:
        tk = yf.Ticker(ticker)
        cf = tk.cashflow.T if hasattr(tk.cashflow, 'T') else pd.DataFrame()
        div = tk.dividends.to_frame(name="dividend") if not tk.dividends.empty else pd.DataFrame()
        income = tk.financials.T if hasattr(tk.financials, 'T') else pd.DataFrame()
        info = tk.info
        return cf, div, info, income
    except Exception as e:
        st.error(f"Yahoo Finance error: {e}")
        return pd.DataFrame(), pd.DataFrame(), {}, pd.DataFrame()

def calc_owner_earnings(cf: pd.DataFrame) -> pd.Series:
    if cf.empty:
        return pd.Series()
    cfo_cols = ["operatingCashFlow", "Total Cash From Operating Activities", "netCashProvidedByOperatingActivities"]
    capex_cols = ["capitalExpenditure", "Capital Expenditures", "capitalExpenditures"]
    cfo = None
    capex = None
    for col in cfo_cols:
        if col in cf.columns:
            cfo = cf[col]
            break
    for col in capex_cols:
        if col in cf.columns:
            capex = cf[col]
            break
    if cfo is not None and capex is not None:
        try:
            return (cfo + capex).astype(float)
        except:
            return pd.Series()
    return pd.Series()

def discounted_cash_flow(last_owner_earnings: float, growth_rates, discount_rate, terminal_growth, shares_outstanding):
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

def dividend_discount_model(last_dividend: float, dividend_growth: float, discount_rate: float) -> float:
    if last_dividend <= 0 or discount_rate <= dividend_growth:
        return 0
    next_div = last_dividend * (1 + dividend_growth)
    return next_div / (discount_rate - dividend_growth)

# --- UI ---
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
shares_out = profile.get("sharesOutstanding") or profile.get("mktCap", 0) / max(profile.get("previousClose", 1), 1)
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

glass_card("""
<h2>Valuation Page</h2>
<p>Run DCF, DDM, and more. (UI/logic to be implemented.)</p>
""")
