"""Streamlit Intrinsic Value Calculator — Enhanced NSE Edition v0.3

New in v0.3:
• Historical valuation trends & peer comparison
• Sensitivity analysis with heatmaps
• Multiple scenario modeling (Bull/Base/Bear)
• Export functionality (Excel/CSV)
• Advanced charts and analytics
• Risk metrics and financial ratios

> Setup

1. pip install streamlit pandas yfinance requests plotly openpyxl
2. Grab a free key at https://financialmodelingprep.com
3. export FMP_API_KEY="YOUR_KEY" (or add to Streamlit Secrets)
4. streamlit run intrinsic_value_app.py
"""

from __future__ import annotations

import math
import os
import io
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import List, Tuple, Dict, Optional

import pandas as pd
import requests
import streamlit as st
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import supported_fmp_tickers

# ────────────────────────────────────────────────────────────────────────
# 💾 ──────────────────────────  Data Layer  ─────────────────────────────
# ────────────────────────────────────────────────────────────────────────

@st.cache_data(ttl=3600)  # Cache for 1 hour
def _fetch_fmp_json(endpoint: str, ticker: str, api_key: str, params: dict | None = None):
    base = "https://financialmodelingprep.com/api/v3"
    url = f"{base}/{endpoint}/{ticker}"
    p = {"apikey": api_key}
    if params:
        p.update(params)
    # Use '&apikey=' if params already exist
    if '?' in url:
        url += f"&apikey={api_key}"
    else:
        url += f"?apikey={api_key}"
    r = requests.get(url, params=p, timeout=15)
    if r.status_code == 403:
        st.error("FMP API returned 403 Forbidden. Check your API key, usage limits, or endpoint.")
        st.stop()
    r.raise_for_status()
    return r.json()

@st.cache_data(ttl=3600)
def fetch_fundamentals_fmp(ticker: str, api_key: str) -> Tuple[pd.DataFrame, pd.DataFrame, dict, pd.DataFrame]:
    """Return (cashflow_df, dividends_df, profile_dict, income_df)."""
    # 1️⃣ Cash‑flow (annual, last 10y)
    cf_json = _fetch_fmp_json("cash-flow-statement", ticker, api_key, {"period": "annual", "limit": 10})
    cf_df = pd.DataFrame(cf_json)
    if not cf_df.empty and "calendarYear" in cf_df.columns:
        cf_df = cf_df.set_index("calendarYear").sort_index()

    # 2️⃣ Income Statement (for ratios)
    try:
        income_json = _fetch_fmp_json("income-statement", ticker, api_key, {"period": "annual", "limit": 10})
        income_df = pd.DataFrame(income_json)
        if not income_df.empty and "calendarYear" in income_df.columns:
            income_df = income_df.set_index("calendarYear").sort_index()
        else:
            income_df = pd.DataFrame()
    except:
        income_df = pd.DataFrame()

    # 3️⃣ Dividends (full history)
    try:
        div_json = _fetch_fmp_json("historical-price-full/stock_dividend", ticker, api_key)
        div_data = div_json.get("historical", [])
        div_df = pd.DataFrame(div_data)
        if not div_df.empty and "date" in div_df.columns:
            div_df = div_df.set_index("date").sort_index()
        else:
            div_df = pd.DataFrame()
    except:
        div_df = pd.DataFrame()

    # 4️⃣ Profile (shares outstanding, etc.)
    try:
        profile_data = _fetch_fmp_json("profile", ticker, api_key)
        profile = profile_data[0] if profile_data else {}
    except:
        profile = {}

    # 5️⃣ Quote (LTP)
    try:
        quote_data = _fetch_fmp_json("quote-short", ticker, api_key)
        quote = quote_data[0] if quote_data else {}
        profile.update(quote)  # merge for convenience
    except:
        pass

    return cf_df, div_df, profile, income_df

@st.cache_data(ttl=3600)
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
    
    # Try different column name variations
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

@st.cache_data(ttl=3600)
def fetch_peer_data(sector: str, api_key: str) -> Dict[str, float]:
    """Fetch peer comparison data - simplified for demo"""
    # Common NSE large caps by sector for demo
    peer_groups = {
        "Technology": ["TCS.NS", "INFY.NS", "HCLTECH.NS", "WIPRO.NS"],
        "Banking": ["HDFCBANK.NS", "ICICIBANK.NS", "KOTAKBANK.NS", "AXISBANK.NS"],
        "Oil & Gas": ["RELIANCE.NS", "ONGC.NS", "IOC.NS", "BPCL.NS"],
        "Auto": ["MARUTI.NS", "TATAMOTORS.NS", "M&M.NS", "BAJAJ-AUTO.NS"]
    }
    
    peers = peer_groups.get(sector, ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS"])
    peer_data = {}
    
    for peer in peers:
        try:
            tk = yf.Ticker(peer)
            info = tk.info
            pe = info.get('trailingPE', 0)
            if pe and pe > 0:
                peer_data[peer.replace('.NS', '')] = pe
        except:
            continue
    
    return peer_data

# ────────────────────────────────────────────────────────────────────────
# 📈 ──────────────────────────  Valuation  ──────────────────────────────
# ────────────────────────────────────────────────────────────────────────

@dataclass
class DCFSettings:
    growth_rates: List[float]
    discount_rate: float
    terminal_growth: float
    shares_outstanding: float

@dataclass
class ScenarioSettings:
    name: str
    growth_multiplier: float
    discount_rate_adj: float
    terminal_growth_adj: float

def discounted_cash_flow(last_owner_earnings: float, settings: DCFSettings) -> float:
    if math.isnan(last_owner_earnings) or last_owner_earnings <= 0:
        return math.nan
    
    flows = []
    oe = last_owner_earnings
    for g in settings.growth_rates:
        oe *= (1 + g)
        flows.append(oe)
    
    # Terminal value
    terminal_value = flows[-1] * (1 + settings.terminal_growth) / (
        settings.discount_rate - settings.terminal_growth
    )
    flows.append(terminal_value)
    
    # Present value calculation
    pv = sum(f / (1 + settings.discount_rate) ** (i + 1) for i, f in enumerate(flows))
    return pv / settings.shares_outstanding if settings.shares_outstanding else math.nan

@dataclass
class DDMSettings:
    dividend_growth: float
    discount_rate: float

def dividend_discount_model(last_dividend: float, settings: DDMSettings) -> float:
    if last_dividend <= 0 or settings.discount_rate <= settings.dividend_growth:
        return 0
    
    next_div = last_dividend * (1 + settings.dividend_growth)
    return next_div / (settings.discount_rate - settings.dividend_growth)

def calculate_historical_valuations(cf_df: pd.DataFrame, div_df: pd.DataFrame, 
                                  base_settings: DCFSettings, ddm_settings: DDMSettings) -> pd.DataFrame:
    """Calculate historical intrinsic values"""
    historical_vals = []
    owner_earnings = calc_owner_earnings(cf_df)
    
    if owner_earnings.empty:
        return pd.DataFrame()
    
    for year in owner_earnings.index[-5:]:  # Last 5 years
        if year in owner_earnings.index:
            oe = owner_earnings.loc[year]
            
            # DCF calculation
            dcf_val = discounted_cash_flow(oe, base_settings)
            
            # DDM calculation (get dividend for that year)
            div_val = 0
            year_divs = div_df[div_df.index.str.startswith(str(year))]
            if not year_divs.empty:
                annual_div = year_divs['dividend'].sum()
                div_val = dividend_discount_model(annual_div, ddm_settings)
            
            fair_val = (dcf_val + div_val) / 2 if not math.isnan(dcf_val) else div_val
            
            historical_vals.append({
                'Year': year,
                'DCF_Value': dcf_val,
                'DDM_Value': div_val,
                'Fair_Value': fair_val
            })
    
    return pd.DataFrame(historical_vals)

def sensitivity_analysis(last_oe: float, last_div: float, base_dcf: DCFSettings, base_ddm: DDMSettings) -> pd.DataFrame:
    """Perform sensitivity analysis on key variables"""
    discount_rates = [base_dcf.discount_rate + i*0.01 for i in range(-3, 4)]
    growth_rates = [base_dcf.growth_rates[0] + i*0.02 for i in range(-3, 4)]
    
    sensitivity_data = []
    
    for dr in discount_rates:
        for gr in growth_rates:
            new_growth_rates = [gr] * 3 + [gr * 0.7] * 4 + [gr * 0.5] * 3
            new_settings = DCFSettings(
                growth_rates=new_growth_rates,
                discount_rate=dr,
                terminal_growth=base_dcf.terminal_growth,
                shares_outstanding=base_dcf.shares_outstanding
            )
            
            dcf_val = discounted_cash_flow(last_oe, new_settings)
            ddm_val = dividend_discount_model(last_div, DDMSettings(base_ddm.dividend_growth, dr))
            fair_val = (dcf_val + ddm_val) / 2 if not math.isnan(dcf_val) else ddm_val
            
            sensitivity_data.append({
                'Discount_Rate': f"{dr:.1%}",
                'Growth_Rate': f"{gr:.1%}",
                'Fair_Value': fair_val
            })
    
    return pd.DataFrame(sensitivity_data)

def calculate_financial_ratios(income_df: pd.DataFrame, profile: dict) -> dict:
    """Calculate key financial ratios"""
    ratios = {}
    
    if not income_df.empty and income_df.shape[0] > 0:
        latest_year = income_df.index[-1]
        
        # Get latest year data
        revenue = income_df.loc[latest_year].get('revenue', 0)
        net_income = income_df.loc[latest_year].get('netIncome', 0)
        
        # Calculate ratios
        market_cap = profile.get('mktCap', 0)
        price = profile.get('price', 0)
        
        if revenue > 0:
            ratios['P/S Ratio'] = market_cap / revenue if market_cap else 0
        if net_income > 0:
            ratios['P/E Ratio'] = market_cap / net_income if market_cap else 0
            ratios['Net Margin'] = net_income / revenue if revenue else 0
        
        # Revenue growth (if we have multiple years)
        if len(income_df) > 1:
            prev_revenue = income_df.iloc[-2].get('revenue', 0)
            if prev_revenue > 0:
                ratios['Revenue Growth'] = (revenue - prev_revenue) / prev_revenue
    
    return ratios

# ────────────────────────────────────────────────────────────────────────
# 📊 ─────────────────────────  Visualization  ────────────────────────────
# ────────────────────────────────────────────────────────────────────────

def create_valuation_chart(historical_df: pd.DataFrame):
    """Create historical valuation trend chart"""
    if historical_df.empty:
        return None
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=historical_df['Year'],
        y=historical_df['DCF_Value'],
        mode='lines+markers',
        name='DCF Value',
        line=dict(color='#1f77b4')
    ))
    
    fig.add_trace(go.Scatter(
        x=historical_df['Year'],
        y=historical_df['DDM_Value'],
        mode='lines+markers',
        name='DDM Value',
        line=dict(color='#ff7f0e')
    ))
    
    fig.add_trace(go.Scatter(
        x=historical_df['Year'],
        y=historical_df['Fair_Value'],
        mode='lines+markers',
        name='Fair Value',
        line=dict(color='#2ca02c', width=3)
    ))
    
    fig.update_layout(
        title='Historical Intrinsic Value Trends',
        xaxis_title='Year',
        yaxis_title='Value (₹)',
        hovermode='x unified'
    )
    
    return fig

def create_sensitivity_heatmap(sensitivity_df: pd.DataFrame):
    """Create sensitivity analysis heatmap"""
    if sensitivity_df.empty:
        return None
    
    # Pivot the data for heatmap
    pivot_df = sensitivity_df.pivot(index='Growth_Rate', columns='Discount_Rate', values='Fair_Value')
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_df.values,
        x=pivot_df.columns,
        y=pivot_df.index,
        colorscale='RdYlGn',
        text=pivot_df.values.round(0),
        texttemplate="%{text}",
        textfont={"size": 10},
        hovertemplate='Discount Rate: %{x}<br>Growth Rate: %{y}<br>Fair Value: ₹%{z:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Sensitivity Analysis: Fair Value vs Growth & Discount Rates',
        xaxis_title='Discount Rate',
        yaxis_title='Growth Rate'
    )
    
    return fig

def create_peer_comparison_chart(peer_data: Dict[str, float], current_pe: float, ticker: str):
    """Create peer comparison chart"""
    if not peer_data:
        return None
    
    companies = list(peer_data.keys()) + [ticker.replace('.NS', '')]
    pe_ratios = list(peer_data.values()) + [current_pe]
    colors = ['lightblue'] * len(peer_data) + ['red']
    
    fig = go.Figure(data=go.Bar(
        x=companies,
        y=pe_ratios,
        marker_color=colors,
        text=[f"{pe:.1f}" for pe in pe_ratios],
        textposition='auto'
    ))
    
    fig.update_layout(
        title='P/E Ratio Peer Comparison',
        xaxis_title='Company',
        yaxis_title='P/E Ratio'
    )
    
    return fig

# ────────────────────────────────────────────────────────────────────────
# 📤 ─────────────────────────  Export Functions  ─────────────────────────
# ────────────────────────────────────────────────────────────────────────

def create_excel_report(ticker: str, valuations: dict, ratios: dict, historical_df: pd.DataFrame, 
                       sensitivity_df: pd.DataFrame) -> bytes:
    """Create comprehensive Excel report"""
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Summary sheet
        summary_data = {
            'Metric': ['DCF Value', 'DDM Value', 'Fair Value', 'Target Price', 'Current Price', 'Upside %'],
            'Value': [
                valuations.get('dcf_val', 0),
                valuations.get('ddm_val', 0),
                valuations.get('fair_val', 0),
                valuations.get('target_price', 0),
                valuations.get('current_price', 0),
                valuations.get('upside', 0)
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # Ratios sheet
        if ratios:
            ratios_df = pd.DataFrame(list(ratios.items()), columns=['Ratio', 'Value'])
            ratios_df.to_excel(writer, sheet_name='Financial_Ratios', index=False)
        
        # Historical valuations
        if not historical_df.empty:
            historical_df.to_excel(writer, sheet_name='Historical_Valuations', index=False)
        
        # Sensitivity analysis
        if not sensitivity_df.empty:
            sensitivity_df.to_excel(writer, sheet_name='Sensitivity_Analysis', index=False)
    
    output.seek(0)
    return output.getvalue()

# ────────────────────────────────────────────────────────────────────────
# 🧮 ───────────────────────  Streamlit  UI  ─────────────────────────────
# ────────────────────────────────────────────────────────────────────────

def main():
    st.set_page_config("Enhanced Intrinsic Value Calculator", layout="wide")
    st.title("📊 Enhanced Intrinsic Value Calculator — NSE Edition v0.3")
    
    # ── Sidebar Inputs ───────────────────────────────────────────────
    with st.sidebar:
        st.header("1️⃣  Stock & Data Source")
        provider = st.selectbox("Data provider", ["Financial Modeling Prep", "Yahoo Finance"], index=0)
        if provider == "Financial Modeling Prep":
            ticker = st.selectbox(
                "Select Ticker (FMP supported)",
                supported_fmp_tickers.supported_fmp_tickers,
                index=0,
                help="Only US, UK, and CA large caps are supported on FMP free plan."
            )
        else:
            ticker = st.text_input("Ticker (e.g., INFY.NS)", "INFY.NS")
        api_key = os.getenv("FMP_API_KEY", "demo")
        if provider == "Financial Modeling Prep" and api_key == "demo":
            st.warning("Using FMP demo key (shared, limited calls). Set FMP_API_KEY env var for your own key.")

        # FMP free plan: only US, UK, CA stocks supported
        unsupported_fmp = False
        if provider == "Financial Modeling Prep":
            if ticker.upper().endswith(".NS") or ticker.upper().endswith(".BO") or \
               ticker.upper().endswith(".AX") or ticker.upper().endswith(".TO") or \
               ticker.upper().endswith(".HK") or ticker.upper().endswith(".SZ") or ticker.upper().endswith(".SS"):
                unsupported_fmp = True
                st.error("FMP free plan only supports US, UK, and CA stocks. For NSE/BSE/other tickers, use Yahoo Finance as the data provider.")

        st.divider()
        st.header("2️⃣  Analysis Mode")
        analysis_mode = st.selectbox("Select analysis", 
                                   ["Basic Valuation", "Scenario Analysis", "Peer Comparison", "Comprehensive Report"])

        st.divider()
        st.header("3️⃣  DCF Assumptions")
        discount_rate = st.slider("Discount rate (%)", 6.0, 20.0, 12.0) / 100
        terminal_growth = st.slider("Terminal growth (%)", 0.0, 5.0, 2.0) / 100
        
        if analysis_mode == "Scenario Analysis":
            st.subheader("Scenario Settings")
            base_growth = st.number_input("Base case growth (%)", 0.0, 30.0, 12.0)
            bull_multiplier = st.slider("Bull case multiplier", 1.0, 2.0, 1.5)
            bear_multiplier = st.slider("Bear case multiplier", 0.3, 1.0, 0.7)
        else:
            base_growth = st.number_input("Growth yrs 1‑3 (%)", 0.0, 30.0, 12.0)
            mid_growth = st.number_input("Growth yrs 4‑7 (%)", 0.0, 20.0, 8.0)
            tail_growth = st.number_input("Growth yrs 8‑10 (%)", 0.0, 10.0, 5.0)

        st.divider()
        st.header("4️⃣  DDM Assumptions")
        div_growth = st.slider("Dividend growth (%)", 0.0, 15.0, 8.0) / 100

        st.divider()
        mos = st.slider("Margin of safety (%)", 0, 50, 20)

    # ── Fetch Data ───────────────────────────────────────────────────
    if not ticker:
        st.info("Please enter a ticker symbol to begin analysis.")
        return

    if provider == "Financial Modeling Prep" and unsupported_fmp:
        st.stop()

    try:
        with st.spinner("Fetching data..."):
            if provider.startswith("Financial"):
                cf_df, div_df, profile, income_df = fetch_fundamentals_fmp(ticker, api_key)
            else:
                cf_df, div_df, profile, income_df = fetch_fundamentals_yahoo(ticker)
    except Exception as e:
        st.error(f"Data fetch failed: {e}")
        st.stop()

    # Extract key metrics
    shares_out = profile.get("sharesOutstanding") or profile.get("mktCap", 0) / max(profile.get("price", 1), 1)
    if not shares_out:
        shares_out = 1e9  # Default fallback
        
    last_price = profile.get("price") or profile.get("previousClose") or math.nan
    
    # Calculate financial ratios
    ratios = calculate_financial_ratios(income_df, profile)

    owner_earnings_series = calc_owner_earnings(cf_df)
    last_oe = owner_earnings_series.iloc[-1] if not owner_earnings_series.empty else math.nan
    last_div = div_df["dividend"].iloc[-1] if not div_df.empty and "dividend" in div_df.columns else 0

    # ── Scenario Analysis ────────────────────────────────────────────
    if analysis_mode == "Scenario Analysis":
        scenarios = [
            ScenarioSettings("Bear", bear_multiplier, 0.02, -0.005),
            ScenarioSettings("Base", 1.0, 0.0, 0.0),
            ScenarioSettings("Bull", bull_multiplier, -0.01, 0.005)
        ]
        
        scenario_results = []
        
        for scenario in scenarios:
            adj_growth = base_growth / 100 * scenario.growth_multiplier
            growth_rates = [adj_growth] * 3 + [adj_growth * 0.7] * 4 + [adj_growth * 0.5] * 3
            
            dcf_settings = DCFSettings(
                growth_rates=growth_rates,
                discount_rate=discount_rate + scenario.discount_rate_adj,
                terminal_growth=terminal_growth + scenario.terminal_growth_adj,
                shares_outstanding=shares_out
            )
            
            dcf_val = discounted_cash_flow(last_oe, dcf_settings) if not math.isnan(last_oe) else math.nan
            ddm_val = dividend_discount_model(last_div, DDMSettings(div_growth, discount_rate + scenario.discount_rate_adj))
            
            fair = (dcf_val + ddm_val) / 2 if not math.isnan(dcf_val) and ddm_val > 0 else (dcf_val if not math.isnan(dcf_val) else ddm_val)
            target = fair * (1 - mos / 100) if not math.isnan(fair) else math.nan
            upside = ((fair - last_price) / last_price * 100) if not math.isnan(fair) and not math.isnan(last_price) and last_price > 0 else math.nan
            
            scenario_results.append({
                'Scenario': scenario.name,
                'DCF Value': dcf_val,
                'DDM Value': ddm_val,
                'Fair Value': fair,
                'Target Price': target,
                'Upside %': upside
            })
        
        # Display scenario results
        st.header("📈 Scenario Analysis")
        scenario_df = pd.DataFrame(scenario_results)
        
        # Format the dataframe for display
        formatted_scenario = scenario_df.copy()
        for col in ['DCF Value', 'DDM Value', 'Fair Value', 'Target Price']:
            formatted_scenario[col] = formatted_scenario[col].apply(lambda x: f"₹ {x:,.0f}" if not math.isnan(x) else "—")
        formatted_scenario['Upside %'] = formatted_scenario['Upside %'].apply(lambda x: f"{x:+.1f}%" if not math.isnan(x) else "—")
        
        st.dataframe(formatted_scenario, use_container_width=True)
        
    else:
        # Regular growth rates for other modes
        growth_rates = [base_growth / 100] * 3 + [mid_growth / 100] * 4 + [tail_growth / 100] * 3

        # ── Standard Valuations ──────────────────────────────────────────
        dcf_val = discounted_cash_flow(
            last_owner_earnings=last_oe,
            settings=DCFSettings(
                growth_rates=growth_rates,
                discount_rate=discount_rate,
                terminal_growth=terminal_growth,
                shares_outstanding=shares_out,
            ),
        ) if not math.isnan(last_oe) else math.nan

        ddm_val = dividend_discount_model(
            last_dividend=last_div,
            settings=DDMSettings(dividend_growth=div_growth, discount_rate=discount_rate),
        )

        # Calculate fair value
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

        # Store valuations for export
        valuations = {
            'dcf_val': dcf_val,
            'ddm_val': ddm_val,
            'fair_val': fair,
            'target_price': target_price,
            'current_price': last_price,
            'upside': upside
        }

        # ── Display Main Results ─────────────────────────────────────────
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("DCF Value", f"₹ {dcf_val:,.0f}" if not math.isnan(dcf_val) else "—")
        with col2:
            st.metric("DDM Value", f"₹ {ddm_val:,.0f}" if ddm_val > 0 else "—")
        with col3:
            st.metric("Avg Fair Value", f"₹ {fair:,.0f}" if not math.isnan(fair) else "—")
        with col4:
            st.metric("MOS Price", f"₹ {target_price:,.0f}" if not math.isnan(target_price) else "—")
        with col5:
            upside_color = "normal" if math.isnan(upside) or upside < 0 else "inverse"
            st.metric("Upside %", f"{upside:+.1f}%" if not math.isnan(upside) else "—", delta_color=upside_color)

        # ── Additional Analysis Based on Mode ────────────────────────────
        if analysis_mode == "Peer Comparison":
            st.header("🏢 Peer Comparison")
            sector = st.selectbox("Select sector", ["Technology", "Banking", "Oil & Gas", "Auto"])
            
            with st.spinner("Fetching peer data..."):
                peer_data = fetch_peer_data(sector, api_key)
                current_pe = ratios.get('P/E Ratio', 0)
                
                if peer_data and current_pe:
                    peer_chart = create_peer_comparison_chart(peer_data, current_pe, ticker)
                    if peer_chart:
                        st.plotly_chart(peer_chart, use_container_width=True)
                    
                    # Peer metrics table
                    peer_df = pd.DataFrame(list(peer_data.items()), columns=['Company', 'P/E Ratio'])
                    peer_df = pd.concat([peer_df, pd.DataFrame({'Company': [ticker.replace('.NS', '')], 'P/E Ratio': [current_pe]})], ignore_index=True)
                    peer_df['Relative Valuation'] = peer_df['P/E Ratio'].apply(
                        lambda x: "Undervalued" if x < peer_df['P/E Ratio'].median() else "Overvalued"
                    )
                    st.dataframe(peer_df, use_container_width=True)
                else:
                    st.info("Peer data not available for comparison.")

        elif analysis_mode == "Comprehensive Report":
            # ── Historical Valuations ────────────────────────────────────
            st.header("📈 Historical Valuation Trends")
            base_dcf_settings = DCFSettings(growth_rates, discount_rate, terminal_growth, shares_out)
            base_ddm_settings = DDMSettings(div_growth, discount_rate)
            
            historical_df = calculate_historical_valuations(cf_df, div_df, base_dcf_settings, base_ddm_settings)
            
            if not historical_df.empty:
                hist_chart = create_valuation_chart(historical_df)
                if hist_chart:
                    st.plotly_chart(hist_chart, use_container_width=True)
                
                # Show historical data table
                with st.expander("Historical Valuation Data"):
                    formatted_hist = historical_df.copy()
                    for col in ['DCF_Value', 'DDM_Value', 'Fair_Value']:
                        formatted_hist[col] = formatted_hist[col].apply(lambda x: f"₹ {x:,.0f}" if not math.isnan(x) else "—")
                    st.dataframe(formatted_hist, use_container_width=True)
            else:
                st.info("Insufficient historical data for trend analysis.")

            # ── Sensitivity Analysis ─────────────────────────────────────
            st.header("🌡️ Sensitivity Analysis")
            with st.spinner("Calculating sensitivity..."):
                sensitivity_df = sensitivity_analysis(last_oe, last_div, base_dcf_settings, base_ddm_settings)
                
                if not sensitivity_df.empty:
                    sens_chart = create_sensitivity_heatmap(sensitivity_df)
                    if sens_chart:
                        st.plotly_chart(sens_chart, use_container_width=True)
                    
                    st.info("💡 **Interpretation:** Green areas indicate higher valuations, red areas indicate lower valuations. This helps understand how sensitive your valuation is to changes in key assumptions.")
                    
                    # Show sensitivity stats
                    pivot_df = sensitivity_df.pivot(index='Growth_Rate', columns='Discount_Rate', values='Fair_Value')
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Min Valuation", f"₹ {pivot_df.min().min():,.0f}")
                    with col2:
                        st.metric("Max Valuation", f"₹ {pivot_df.max().max():,.0f}")
                    with col3:
                        valuation_range = pivot_df.max().max() - pivot_df.min().min()
                        st.metric("Valuation Range", f"₹ {valuation_range:,.0f}")

    # ── Financial Ratios & Risk Metrics ──────────────────────────────
    if ratios and analysis_mode in ["Basic Valuation", "Comprehensive Report"]:
        st.header("📊 Financial Ratios & Risk Metrics")
        
        ratio_cols = st.columns(len(ratios))
        for i, (ratio_name, ratio_value) in enumerate(ratios.items()):
            with ratio_cols[i]:
                if isinstance(ratio_value, float):
                    if "Growth" in ratio_name or "Margin" in ratio_name:
                        display_val = f"{ratio_value:.1%}"
                    else:
                        display_val = f"{ratio_value:.2f}"
                else:
                    display_val = str(ratio_value)
                st.metric(ratio_name, display_val)

    # ── Charts Section ───────────────────────────────────────────────
    if analysis_mode in ["Basic Valuation", "Comprehensive Report"]:
        st.header("📈 Financial Charts")
        
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.subheader("Owner Earnings Trend")
            if not owner_earnings_series.empty and len(owner_earnings_series) > 0:
                # Create interactive chart
                oe_df = owner_earnings_series.tail(10).reset_index()
                oe_df.columns = ['Year', 'Owner_Earnings']
                oe_df['Owner_Earnings_Billions'] = oe_df['Owner_Earnings'] / 1e9
                
                fig_oe = px.bar(oe_df, x='Year', y='Owner_Earnings_Billions',
                               title="Owner Earnings (₹ Billions)",
                               color='Owner_Earnings_Billions',
                               color_continuous_scale='viridis')
                fig_oe.update_layout(showlegend=False)
                st.plotly_chart(fig_oe, use_container_width=True)
                
                # Growth analysis
                if len(owner_earnings_series) > 1:
                    recent_growth = ((owner_earnings_series.iloc[-1] / owner_earnings_series.iloc[-2]) - 1) * 100
                    st.info(f"📈 Recent YoY Owner Earnings Growth: **{recent_growth:+.1f}%**")
            else:
                st.info("No cash‑flow data available for this ticker.")

        with chart_col2:
            st.subheader("Dividend History")
            if not div_df.empty and "dividend" in div_df.columns and len(div_df) > 0:
                div_chart_df = div_df.tail(20).reset_index()
                div_chart_df['date'] = pd.to_datetime(div_chart_df['date'])
                
                fig_div = px.line(div_chart_df, x='date', y='dividend',
                                 title="Dividend Per Share (₹)",
                                 markers=True)
                fig_div.update_traces(line_color='orange', marker_color='orange')
                st.plotly_chart(fig_div, use_container_width=True)
                
                # Dividend analysis
                if len(div_df) > 1:
                    annual_divs = div_df.groupby(div_df.index.str[:4])['dividend'].sum()
                    if len(annual_divs) > 1:
                        div_growth_rate = ((annual_divs.iloc[-1] / annual_divs.iloc[-2]) - 1) * 100
                        st.info(f"💰 Recent Annual Dividend Growth: **{div_growth_rate:+.1f}%**")
            else:
                st.info("No dividend data available.")

    # ── Export Functionality ─────────────────────────────────────────
    if analysis_mode == "Comprehensive Report":
        st.header("📤 Export Report")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Download Excel Report", type="primary"):
                try:
                    excel_data = create_excel_report(
                        ticker, valuations, ratios, 
                        historical_df if 'historical_df' in locals() else pd.DataFrame(),
                        sensitivity_df if 'sensitivity_df' in locals() else pd.DataFrame()
                    )
                    
                    st.download_button(
                        label="💾 Download Excel File",
                        data=excel_data,
                        file_name=f"{ticker.replace('.NS', '')}_valuation_report_{date.today().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                except Exception as e:
                    st.error(f"Export failed: {e}")
        
        with col2:
            if st.button("📄 Download CSV Summary"):
                try:
                    summary_data = {
                        'Metric': ['DCF Value', 'DDM Value', 'Fair Value', 'Target Price', 'Current Price', 'Upside %'],
                        'Value': [
                            valuations.get('dcf_val', 0),
                            valuations.get('ddm_val', 0), 
                            valuations.get('fair_val', 0),
                            valuations.get('target_price', 0),
                            valuations.get('current_price', 0),
                            valuations.get('upside', 0)
                        ]
                    }
                    summary_df = pd.DataFrame(summary_data)
                    csv_data = summary_df.to_csv(index=False)
                    
                    st.download_button(
                        label="💾 Download CSV File",
                        data=csv_data,
                        file_name=f"{ticker.replace('.NS', '')}_valuation_summary_{date.today().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                except Exception as e:
                    st.error(f"CSV export failed: {e}")

    # ── Risk Warnings & Disclaimers ──────────────────────────────────
    with st.expander("⚠️ Risk Warnings & Model Limitations"):
        st.warning("""
        **Important Disclaimers:**
        
        1. **Model Limitations**: DCF and DDM models are simplified representations. Real valuations depend on numerous factors not captured here.
        
        2. **Assumption Sensitivity**: Small changes in growth rates, discount rates, or terminal values can significantly impact valuations.
        
        3. **Historical Performance**: Past performance does not guarantee future results. Historical trends may not continue.
        
        4. **Market Conditions**: Valuations don't account for market sentiment, macroeconomic factors, or sector-specific risks.
        
        5. **Data Quality**: Results depend on the accuracy and completeness of financial data from external providers.
        
        6. **Investment Decision**: This tool is for educational purposes only. Consult qualified financial advisors before making investment decisions.
        """)

    # ── Footer Information ───────────────────────────────────────────
    st.divider()
    
    info_col1, info_col2, info_col3 = st.columns(3)
    
    with info_col1:
        if not math.isnan(last_price):
            st.info(f"**Current Price:** ₹ {last_price:,.2f}")
    
    with info_col2:
        st.info(f"**Shares Outstanding:** {shares_out:,.0f}")
    
    with info_col3:
        market_cap = shares_out * last_price if not math.isnan(last_price) else 0
        if market_cap > 0:
            st.info(f"**Market Cap:** ₹ {market_cap/1e9:,.1f}B")

    st.caption(f"📡 Data via {provider} • 🗓️ Last refresh: {datetime.now().strftime('%Y-%m-%d %H:%M')} • ⚖️ For educational purposes only")

    # ── Quick Tips Sidebar ───────────────────────────────────────────
    with st.sidebar:
        st.divider()
        st.header("💡 Quick Tips")
        
        tips = [
            "🎯 Use 'Comprehensive Report' for detailed analysis",
            "📊 Try 'Scenario Analysis' to test different assumptions", 
            "🏢 'Peer Comparison' helps assess relative valuation",
            "🌡️ Sensitivity analysis shows assumption impact",
            "📤 Export reports for further analysis",
            "⚠️ Always cross-check with fundamental analysis"
        ]
        
        for tip in tips:
            st.write(tip)

if __name__ == "__main__":
    main()