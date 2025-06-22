"""Streamlit Intrinsic Value Calculator — Modern UI Edition v0.4

New in v0.4:
• Beautiful modern UI with glassmorphism design
• Animated metrics and progress indicators
• Enhanced color schemes and typography
• Interactive dashboard layout
• Modern card-based components
• Responsive design elements

> Setup

1. pip install streamlit pandas requests plotly openpyxl streamlit-option-menu streamlit-elements nsepy
2. Grab a free key at https://financialmodelingprep.com
3. export FMP_API_KEY="YOUR_KEY" (or add to Streamlit Secrets)
4. streamlit run app.py
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
from nsepy import get_history
from datetime import date
import plotly.express as px
from ivnse.models import DCFSettings, discounted_cash_flow
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def main():
    st.set_page_config(
        page_title="Intrinsic Value Calculator",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # The rest of the main app logic will be added here
    # This is just a placeholder for now
    st.write("Intrinsic Value Calculator")
    st.write("Please wait while we set up the app...")

if __name__ == "__main__":
    main()

# ────────────────────────────────────────────────────────────────────────
# 🎨 ──────────────────────────  Modern UI Styling  ──────────────────────
# ────────────────────────────────────────────────────────────────────────

def apply_modern_styling():
    """Apply modern CSS styling with glassmorphism and animations"""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Variables */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --accent-color: #06d6a0;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
        --success-color: #10b981;
        --text-primary: #1f2937;
        --text-secondary: #6b7280;
        --bg-primary: #ffffff;
        --bg-secondary: #f8fafc;
        --bg-glass: rgba(255, 255, 255, 0.25);
        --border-color: rgba(255, 255, 255, 0.18);
        --shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        --border-radius: 16px;
    }
    
    /* Main App Styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        font-family: 'Inter', sans-serif;
    }
    
    /* Custom Header */
    .custom-header {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
        animation: fadeInUp 1s ease-out;
    }
    
    .custom-subheader {
        color: var(--text-secondary);
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 3rem;
        font-weight: 400;
    }
    
    /* Glass Card Design */
    .glass-card {
        background: var(--bg-glass);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: var(--border-radius);
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow);
        padding: 2rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 16px 48px 0 rgba(31, 38, 135, 0.5);
    }
    
    /* Modern Metrics */
    .modern-metric {
        background: linear-gradient(135deg, var(--bg-primary), var(--bg-secondary));
        border-radius: var(--border-radius);
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .modern-metric::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        transition: left 0.5s;
    }
    
    .modern-metric:hover::before {
        left: 100%;
    }
    
    .modern-metric:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        color: var(--text-secondary);
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Animated Progress Bars */
    .progress-container {
        background: #e5e7eb;
        border-radius: 10px;
        height: 8px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
        border-radius: 10px;
        transition: width 1.5s ease-in-out;
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { background-position: -468px 0; }
        100% { background-position: 468px 0; }
    }
    
    /* Navigation Styling */
    .nav-container {
        background: var(--bg-glass);
        backdrop-filter: blur(16px);
        border-radius: var(--border-radius);
        padding: 1rem;
        margin-bottom: 2rem;
        border: 1px solid var(--border-color);
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(99, 102, 241, 0.4);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    /* Chart Container */
    .chart-container {
        background: var(--bg-primary);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .fade-in {
        animation: fadeIn 0.8s ease-out;
    }
    
    .fade-in-up {
        animation: fadeInUp 0.8s ease-out;
    }
    
    /* Status Indicators */
    .status-positive {
        color: var(--success-color);
        background: rgba(16, 185, 129, 0.1);
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .status-negative {
        color: var(--danger-color);
        background: rgba(239, 68, 68, 0.1);
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .status-neutral {
        color: var(--warning-color);
        background: rgba(245, 158, 11, 0.1);
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    /* Info Cards */
    .info-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: var(--border-radius);
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    .warning-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: var(--border-radius);
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(245, 87, 108, 0.3);
    }
    
    /* Hide Streamlit Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--primary-color), var(--secondary-color));
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-color);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .custom-header {
            font-size: 2.5rem;
        }
        
        .modern-metric {
            margin-bottom: 1rem;
        }
        
        .glass-card {
            padding: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def create_modern_header():
    """Create modern animated header"""
    st.markdown("""
    <div class="custom-header">
        📈 Intrinsic Value Calculator
    </div>
    <div class="custom-subheader">
        Professional NSE Stock Valuation with Advanced Analytics
    </div>
    """, unsafe_allow_html=True)

def create_metric_card(label: str, value: str, delta: Optional[str] = None, delta_color: str = "normal"):
    """Create modern metric cards with animations"""
    delta_class = ""
    if delta:
        if delta_color == "inverse":
            delta_class = "status-positive"
        elif "negative" in delta_color or delta.startswith("-"):
            delta_class = "status-negative"
        else:
            delta_class = "status-neutral"
    
    delta_html = f'<div class="{delta_class}">{delta}</div>' if delta else ""
    
    return f"""
    <div class="modern-metric fade-in-up">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
        {delta_html}
    </div>
    """

def create_info_card(title: str, content: str, card_type: str = "info"):
    """Create beautiful info cards"""
    card_class = "info-card" if card_type == "info" else "warning-card"
    
    return f"""
    <div class="{card_class} fade-in">
        <h3 style="margin-top: 0; font-weight: 600;">{title}</h3>
        <p style="margin-bottom: 0; line-height: 1.6;">{content}</p>
    </div>
    """

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
    r = requests.get(url, params=p, timeout=15)
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

@st.cache_data(ttl=3600 * 24)  # Cache for 24 hours
def fetch_peer_data(sector: str, api_key: str) -> Dict[str, float]:
    """Fetch peer comparison data using NSEpy"""
    # Common NSE large caps by sector
    peer_groups = {
        "Technology": ["TCS", "INFY", "HCLTECH", "WIPRO"],
        "Banking": ["HDFCBANK", "ICICIBANK", "KOTAKBANK", "AXISBANK"],
        "Oil & Gas": ["RELIANCE", "ONGC", "IOC", "BPCL"],
        "Auto": ["MARUTI", "TATAMOTORS", "M&M", "BAJAJ-AUTO"]
    }
    
    peers = peer_groups.get(sector, ["RELIANCE", "TCS", "HDFCBANK"])
    peer_data = {}
    
    end_date = date.today()
    start_date = end_date - timedelta(days=30)  # Last 30 days for P/E calculation
    
    for peer in peers:
        try:
            # Get historical data for P/E calculation
            hist = get_history(symbol=peer, start=start_date, end=end_date)
            if hist.empty:
                continue
                
            # Calculate trailing P/E (simplified)
            last_close = hist['Close'].iloc[-1]
            last_eps = hist['Close'].mean() / 20  # Placeholder for EPS
            pe = last_close / last_eps if last_eps > 0 else 0
            
            if pe > 0:
                peer_data[peer] = pe
        except Exception as e:
            print(f"Error fetching data for {peer}: {e}")
            continue
    
    return peer_data

# ────────────────────────────────────────────────────────────────────────
# ──────────────────────────  Valuation Models  ──────────────────────
# ────────────────────────────────────────────────────────────────────────

@dataclass
class ScenarioSettings:
    name: str
    growth_multiplier: float
    discount_rate_adj: float
    terminal_growth_adj: float


@dataclass
class DDMSettings:
    dividend_growth: float
    discount_rate: float

def dividend_discount_model(last_dividend: float, settings: DDMSettings) -> float:
    if last_dividend <= 0 or settings.discount_rate <= settings.dividend_growth:
        return 0
    
    next_div = last_dividend * (1 + settings.dividend_growth)
    return next_div / (settings.discount_rate - settings.dividend_growth)

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
# 📊 ─────────────────────────  Modern Visualizations  ────────────────────
# ────────────────────────────────────────────────────────────────────────

def create_modern_valuation_chart(dcf_val, ddm_val, fair_val, current_price):
    """Create beautiful valuation comparison chart"""
    
    # Create data
    values = [dcf_val, ddm_val, fair_val, current_price]
    labels = ['DCF Value', 'DDM Value', 'Fair Value', 'Current Price']
    colors = ['#6366f1', '#8b5cf6', '#06d6a0', '#f59e0b']
    
    # Filter out NaN values
    valid_data = [(label, value, color) for label, value, color in zip(labels, values, colors) 
                  if not math.isnan(value) and value > 0]
    
    if not valid_data:
        return None
    
    labels_clean, values_clean, colors_clean = zip(*valid_data)
    
    fig = go.Figure()
    
    # Add bars with gradient effect
    fig.add_trace(go.Bar(
        x=labels_clean,
        y=values_clean,
        marker=dict(
            color=colors_clean,
            line=dict(color='rgba(255,255,255,0.3)', width=2)
        ),
        text=[f"₹{v:,.0f}" for v in values_clean],
        textposition='auto',
        textfont=dict(size=14, color='white', family='Inter'),
        hovertemplate='<b>%{x}</b><br>Value: ₹%{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text="💰 Valuation Summary",
            font=dict(size=24, color='#1f2937', family='Inter', weight='bold'),
            x=0.5
        ),
        xaxis=dict(
            showgrid=False,
            tickfont=dict(size=12, color='#6b7280', family='Inter')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)',
            tickfont=dict(size=12, color='#6b7280', family='Inter'),
            title=dict(text="Value (₹)", font=dict(size=14, color='#374151'))
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        margin=dict(t=80, b=40, l=60, r=40)
    )
    
    return fig

def create_modern_owner_earnings_chart(owner_earnings_series):
    """Create modern owner earnings trend chart"""
    if owner_earnings_series.empty:
        return None
    
    oe_df = owner_earnings_series.tail(10).reset_index()
    oe_df.columns = ['Year', 'Owner_Earnings']
    oe_df['Owner_Earnings_Billions'] = oe_df['Owner_Earnings'] / 1e9
    
    fig = go.Figure()
    
    # Add area chart with gradient
    fig.add_trace(go.Scatter(
        x=oe_df['Year'],
        y=oe_df['Owner_Earnings_Billions'],
        mode='lines+markers',
        fill='tonexty',
        fillcolor='rgba(99, 102, 241, 0.2)',
        line=dict(color='#6366f1', width=3),
        marker=dict(size=8, color='#6366f1', symbol='circle'),
        hovertemplate='<b>Year %{x}</b><br>Owner Earnings: ₹%{y:.1f}B<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text="📈 Owner Earnings Trend",
            font=dict(size=20, color='#1f2937', family='Inter', weight='bold'),
            x=0.5
        ),
        xaxis=dict(
            showgrid=False,
            tickfont=dict(size=11, color='#6b7280', family='Inter'),
            title=dict(text="Year", font=dict(size=12, color='#374151'))
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)',
            tickfont=dict(size=11, color='#6b7280', family='Inter'),
            title=dict(text="Owner Earnings (₹ Billions)", font=dict(size=12, color='#374151'))
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=350,
        margin=dict(t=60, b=40, l=60, r=40)
    )
    
    return fig

def create_modern_dividend_chart(div_df):
    """Create modern dividend trend chart"""
    if div_df.empty or "dividend" not in div_df.columns:
        return None
    
    div_chart_df = div_df.tail(20).reset_index()
    div_chart_df['date'] = pd.to_datetime(div_chart_df['date'])
    
    fig = go.Figure()
    
    # Add line with markers
    fig.add_trace(go.Scatter(
        x=div_chart_df['date'],
        y=div_chart_df['dividend'],
        mode='lines+markers',
        line=dict(color='#06d6a0', width=3),
        marker=dict(size=6, color='#06d6a0'),
        hovertemplate='<b>%{x}</b><br>Dividend: ₹%{y:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text="💎 Dividend History",
            font=dict(size=20, color='#1f2937', family='Inter', weight='bold'),
            x=0.5
        ),
        xaxis=dict(
            showgrid=False,
            tickfont=dict(size=11, color='#6b7280', family='Inter'),
            title=dict(text="Date", font=dict(size=12, color='#374151'))
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)',
            tickfont=dict(size=11, color='#6b7280', family='Inter'),
            title=dict(text="Dividend per Share (₹)", font=dict(size=12, color='#374151'))
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=350,
        margin=dict(t=60, b=40, l=60, r=40)
    )
    
    return fig

def create_scenario_comparison_chart(scenario_results):
    """Create beautiful scenario comparison chart"""
    df = pd.DataFrame(scenario_results)
    
    fig = go.Figure()
    
    scenarios = df['Scenario']
    fair_values = df['Fair Value']
    colors = ['#ef4444', '#6366f1', '#10b981']  # Red, Blue, Green
    
    fig.add_trace(go.Bar(
        x=scenarios,
        y=fair_values,
        marker=dict(
            color=colors,
            line=dict(color='white', width=2)
        ),
        text=[f"₹{v:,.0f}" for v in fair_values],
        textposition='auto',
        textfont=dict(size=14, color='white', family='Inter', weight='bold'),
        hovertemplate='<b>%{x} Case</b><br>Fair Value: ₹%{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text="🎯 Scenario Analysis",
            font=dict(size=24, color='#1f2937', family='Inter', weight='bold'),
            x=0.5
        ),
        xaxis=dict(
            showgrid=False,
            tickfont=dict(size=12, color='#6b7280', family='Inter')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)',
            tickfont=dict(size=12, color='#6b7280', family='Inter'),
            title=dict(text="Fair Value (₹)", font=dict(size=14, color='#374151'))
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        margin=dict(t=80, b=40, l=60, r=40)
    )
    
    return fig

def create_sensitivity_heatmap(sensitivity_df: pd.DataFrame):
    """Create beautiful sensitivity analysis heatmap"""
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
        texttemplate="₹%{text:,.0f}",
        textfont={"size": 10, "family": "Inter", "color": "white"},
        hovertemplate='<b>Sensitivity Analysis</b><br>Discount Rate: %{x}<br>Growth Rate: %{y}<br>Fair Value: ₹%{z:,.0f}<extra></extra>',
        colorbar=dict(
            title="Fair Value (₹)",
            titlefont=dict(family="Inter", size=12),
            tickfont=dict(family="Inter", size=10)
        )
    ))
    
    fig.update_layout(
        title=dict(
            text="🌡️ Sensitivity Analysis Heatmap",
            font=dict(size=20, color='#1f2937', family='Inter', weight='bold'),
            x=0.5
        ),
        xaxis=dict(
            title="Discount Rate",
            titlefont=dict(size=12, color='#374151', family='Inter'),
            tickfont=dict(size=10, color='#6b7280', family='Inter')
        ),
        yaxis=dict(
            title="Growth Rate",
            titlefont=dict(size=12, color='#374151', family='Inter'),
            tickfont=dict(size=10, color='#6b7280', family='Inter')
        ),
        height=400,
        margin=dict(t=60, b=40, l=60, r=40)
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
# 🧮 ───────────────────────  Main Application  ─────────────────────────
# ────────────────────────────────────────────────────────────────────────

def main():
    st.set_page_config(
        page_title="Intrinsic Value Calculator",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply modern styling
    apply_modern_styling()
    
    # Create modern header
    create_modern_header()
    
    # ── Modern Sidebar Navigation ────────────────────────────────────────
    with st.sidebar:
        st.markdown('<div class="nav-container">', unsafe_allow_html=True)
        st.markdown("### 🎛️ Control Panel")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Stock Input Section
        st.markdown("#### 1️⃣ Stock Selection")
        ticker = st.text_input(
            "Enter NSE Ticker", 
            value="INFY.NS",
            placeholder="e.g., TCS.NS, RELIANCE.NS",
            help="Enter NSE stock symbol with .NS suffix"
        )
        
        provider = st.selectbox(
            "📊 Data Provider", 
            ["Financial Modeling Prep", "Yahoo Finance"], 
            index=0,
            help="FMP recommended for Indian markets"
        )
        
        api_key = os.getenv("FMP_API_KEY", "demo")
        if provider == "Financial Modeling Prep" and api_key == "demo":
            st.markdown(create_info_card(
                "Demo Mode", 
                "Using shared demo key. Set FMP_API_KEY environment variable for unlimited access.",
                "warning"
            ), unsafe_allow_html=True)

        st.divider()
        
        # Analysis Mode Selection
        st.markdown("#### 2️⃣ Analysis Mode")
        analysis_mode = st.selectbox(
            "🔍 Select Analysis Type", 
            ["🎯 Basic Valuation", "📊 Scenario Analysis", "🏢 Peer Comparison", "📋 Comprehensive Report"],
            help="Choose your analysis depth"
        )

        st.divider()
        
        # DCF Parameters
        st.markdown("#### 3️⃣ DCF Assumptions")
        
        discount_rate = st.slider(
            "💰 Discount Rate (%)", 
            min_value=6.0, max_value=20.0, value=12.0, step=0.5,
            help="Required rate of return (WACC)"
        ) / 100
        
        terminal_growth = st.slider(
            "🚀 Terminal Growth (%)", 
            min_value=0.0, max_value=5.0, value=2.0, step=0.1,
            help="Long-term perpetual growth rate"
        ) / 100
        
        if "Scenario" in analysis_mode:
            st.markdown("##### Scenario Settings")
            base_growth = st.number_input(
                "Base Growth Rate (%)", 
                min_value=0.0, max_value=30.0, value=12.0, step=1.0
            )
            bull_multiplier = st.slider("Bull Case Multiplier", 1.0, 2.0, 1.5, 0.1)
            bear_multiplier = st.slider("Bear Case Multiplier", 0.3, 1.0, 0.7, 0.1)
        else:
            base_growth = st.number_input("Growth Years 1-3 (%)", 0.0, 30.0, 12.0, 1.0)
            mid_growth = st.number_input("Growth Years 4-7 (%)", 0.0, 20.0, 8.0, 1.0)
            tail_growth = st.number_input("Growth Years 8-10 (%)", 0.0, 10.0, 5.0, 1.0)

        st.divider()
        
        # DDM Parameters
        st.markdown("#### 4️⃣ Dividend Model")
        div_growth = st.slider(
            "📈 Dividend Growth (%)", 
            min_value=0.0, max_value=15.0, value=8.0, step=0.5,
            help="Expected annual dividend growth rate"
        ) / 100

        st.divider()
        
        # Risk Settings
        st.markdown("#### 5️⃣ Risk Management")
        mos = st.slider(
            "🛡️ Margin of Safety (%)", 
            min_value=0, max_value=50, value=20, step=5,
            help="Safety buffer for uncertainty"
        )

    # ── Data Fetching with Modern Loading ────────────────────────────────
    if not ticker:
        st.markdown(create_info_card(
            "Welcome! 👋", 
            "Enter a ticker symbol in the sidebar to begin your stock valuation analysis.",
            "info"
        ), unsafe_allow_html=True)
        return

    # Progress bar for data fetching
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("🔄 Fetching financial data...")
        progress_bar.progress(25)
        
        if provider.startswith("Financial"):
            cf_df, div_df, profile, income_df = fetch_fundamentals_fmp(ticker, api_key)
        else:
            cf_df, div_df, profile, income_df = fetch_fundamentals_yahoo(ticker)
        
        progress_bar.progress(75)
        status_text.text("📊 Processing financial metrics...")
        
        # Calculate key metrics
        shares_out = profile.get("sharesOutstanding") or profile.get("mktCap", 0) / max(profile.get("price", 1), 1)
        if not shares_out:
            shares_out = 1e9  # Default fallback
            
        last_price = profile.get("price") or profile.get("previousClose") or math.nan
        
        # Calculate financial ratios
        ratios = calculate_financial_ratios(income_df, profile)
        
        owner_earnings_series = calc_owner_earnings(cf_df)
        last_oe = owner_earnings_series.iloc[-1] if not owner_earnings_series.empty else math.nan
        last_div = div_df["dividend"].iloc[-1] if not div_df.empty and "dividend" in div_df.columns else 0
        
        progress_bar.progress(100)
        status_text.text("✅ Data loaded successfully!")
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        st.error(f"❌ Data fetch failed: {e}")
        st.stop()

    # ── Company Information Header ───────────────────────────────────────
    company_name = profile.get('companyName', ticker.replace('.NS', ''))
    sector = profile.get('sector', 'Unknown')
    
    st.markdown(f"""
    <div class="glass-card">
        <h2 style="margin: 0; color: #1f2937; font-family: 'Inter';">
            📊 {company_name} ({ticker})
        </h2>
        <p style="margin: 0.5rem 0 0 0; color: #6b7280; font-size: 1.1rem;">
            Sector: {sector} | Market Cap: ₹{(shares_out * last_price / 1e9):,.1f}B | Price: ₹{last_price:,.2f}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Main Analysis Based on Mode ──────────────────────────────────────
    if "Scenario" in analysis_mode:
        # Scenario Analysis
        scenarios = [
            ScenarioSettings("🐻 Bear", bear_multiplier, 0.02, -0.005),
            ScenarioSettings("⚖️ Base", 1.0, 0.0, 0.0),
            ScenarioSettings("🐂 Bull", bull_multiplier, -0.01, 0.005)
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

        # Display scenario results with modern styling
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        # Create scenario comparison chart
        scenario_chart = create_scenario_comparison_chart(scenario_results)
        if scenario_chart:
            st.plotly_chart(scenario_chart, use_container_width=True)
        
        # Scenario metrics cards
        cols = st.columns(3)
        for i, result in enumerate(scenario_results):
            with cols[i]:
                scenario_name = result['Scenario']
                fair_value = result['Fair Value']
                upside = result['Upside %']
                
                upside_text = f"{upside:+.1f}%" if not math.isnan(upside) else "—"
                upside_color = "inverse" if not math.isnan(upside) and upside > 0 else "normal"
                
                st.markdown(
                    create_metric_card(
                        scenario_name, 
                        f"₹{fair_value:,.0f}" if not math.isnan(fair_value) else "—",
                        upside_text,
                        upside_color
                    ), 
                    unsafe_allow_html=True
                )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        # Standard Valuation Analysis
        if "Scenario" not in analysis_mode:
            growth_rates = [base_growth / 100] * 3 + [mid_growth / 100] * 4 + [tail_growth / 100] * 3
        
        # Calculate valuations
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

        # ── Display Main Valuation Results ───────────────────────────────
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        # Main valuation chart
        val_chart = create_modern_valuation_chart(dcf_val, ddm_val, fair, last_price)
        if val_chart:
            st.plotly_chart(val_chart, use_container_width=True)
        
        # Metrics row
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown(
                create_metric_card("DCF Value", f"₹{dcf_val:,.0f}" if not math.isnan(dcf_val) else "—"),
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                create_metric_card("DDM Value", f"₹{ddm_val:,.0f}" if ddm_val > 0 else "—"),
                unsafe_allow_html=True
            )
        with col3:
            st.markdown(
                create_metric_card("Fair Value", f"₹{fair:,.0f}" if not math.isnan(fair) else "—"),
                unsafe_allow_html=True
            )
        with col4:
            st.markdown(
                create_metric_card("Target Price", f"₹{target_price:,.0f}" if not math.isnan(target_price) else "—"),
                unsafe_allow_html=True
            )
        with col5:
            upside_text = f"{upside:+.1f}%" if not math.isnan(upside) else "—"
            upside_color = "inverse" if not math.isnan(upside) and upside > 0 else "normal"
            st.markdown(
                create_metric_card("Upside", upside_text, delta_color=upside_color),
                unsafe_allow_html=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Financial Ratios Dashboard ───────────────────────────────────────
    if ratios:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Financial Health Dashboard")
        
        ratio_cols = st.columns(len(ratios))
        for i, (ratio_name, ratio_value) in enumerate(ratios.items()):
            with ratio_cols[i]:
                if isinstance(ratio_value, float):
                    if "Growth" in ratio_name or "Margin" in ratio_name:
                        display_val = f"{ratio_value:.1%}"
                        delta_color = "inverse" if ratio_value > 0 else "normal"
                    else:
                        display_val = f"{ratio_value:.2f}"
                        delta_color = "normal"
                else:
                    display_val = str(ratio_value)
                    delta_color = "normal"
                
                st.markdown(
                    create_metric_card(ratio_name, display_val),
                    unsafe_allow_html=True
                )
        
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Advanced Analysis Sections ───────────────────────────────────────
    if "Comprehensive" in analysis_mode:
        # Sensitivity Analysis
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        # Calculate sensitivity
        base_dcf_settings = DCFSettings(growth_rates if 'growth_rates' in locals() else [0.12]*10, discount_rate, terminal_growth, shares_out)
        base_ddm_settings = DDMSettings(div_growth, discount_rate)
        
        # Simplified sensitivity for performance
        discount_rates = [discount_rate + i*0.01 for i in range(-2, 3)]
        growth_rate_base = growth_rates[0] if 'growth_rates' in locals() else 0.12
        growth_rate_range = [growth_rate_base + i*0.02 for i in range(-2, 3)]
        
        sensitivity_data = []
        for dr in discount_rates:
            for gr in growth_rate_range:
                new_growth_rates = [gr] * 3 + [gr * 0.7] * 4 + [gr * 0.5] * 3
                new_settings = DCFSettings(new_growth_rates, dr, terminal_growth, shares_out)
                
                dcf_sens = discounted_cash_flow(last_oe, new_settings) if not math.isnan(last_oe) else 0
                ddm_sens = dividend_discount_model(last_div, DDMSettings(div_growth, dr))
                fair_sens = (dcf_sens + ddm_sens) / 2 if dcf_sens > 0 and ddm_sens > 0 else (dcf_sens if dcf_sens > 0 else ddm_sens)
                
                sensitivity_data.append({
                    'Discount_Rate': f"{dr:.1%}",
                    'Growth_Rate': f"{gr:.1%}",
                    'Fair_Value': fair_sens
                })
        
        sensitivity_df = pd.DataFrame(sensitivity_data)
        
        sens_chart = create_sensitivity_heatmap(sensitivity_df)
        if sens_chart:
            st.plotly_chart(sens_chart, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Charts Section ───────────────────────────────────────────────────
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        oe_chart = create_modern_owner_earnings_chart(owner_earnings_series)
        if oe_chart:
            st.plotly_chart(oe_chart, use_container_width=True)
            
            # Growth analysis
            if len(owner_earnings_series) > 1:
                recent_growth = ((owner_earnings_series.iloc[-1] / owner_earnings_series.iloc[-2]) - 1) * 100
                growth_status = "positive" if recent_growth > 0 else "negative"
                st.markdown(f"""
                <div class="status-{growth_status}">
                    📈 Recent YoY Growth: {recent_growth:+.1f}%
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("💡 No cash flow data available for earnings analysis.")
        
        st.markdown('</div>', unsafe_allow_html=True)

    with chart_col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        div_chart = create_modern_dividend_chart(div_df)
        if div_chart:
            st.plotly_chart(div_chart, use_container_width=True)
            
            # Dividend analysis
            if not div_df.empty and len(div_df) > 1:
                annual_divs = div_df.groupby(div_df.index.str[:4])['dividend'].sum()
                if len(annual_divs) > 1:
                    div_growth_rate = ((annual_divs.iloc[-1] / annual_divs.iloc[-2]) - 1) * 100
                    growth_status = "positive" if div_growth_rate > 0 else "negative"
                    st.markdown(f"""
                    <div class="status-{growth_status}">
                        💰 Annual Dividend Growth: {div_growth_rate:+.1f}%
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("💡 No dividend data available for this stock.")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Export Section ───────────────────────────────────────────────────
    if "Comprehensive" in analysis_mode:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📤 Export Analysis Report")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Generate Excel Report", type="primary"):
                try:
                    excel_data = create_excel_report(
                        ticker, valuations, ratios, 
                        pd.DataFrame() if 'historical_df' not in locals() else pd.DataFrame(),
                        sensitivity_df if 'sensitivity_df' in locals() else pd.DataFrame()
                    )
                    
                    st.download_button(
                        label="💾 Download Excel File",
                        data=excel_data,
                        file_name=f"{ticker.replace('.NS', '')}_valuation_report_{date.today().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    st.success("✅ Excel report generated successfully!")
                except Exception as e:
                    st.error(f"❌ Export failed: {e}")
        
        with col2:
            if st.button("📄 Generate CSV Summary"):
                try:
                    summary_data = {
                        'Metric': ['DCF Value', 'DDM Value', 'Fair Value', 'Target Price', 'Current Price', 'Upside %'],
                        'Value': [
                            valuations.get('dcf_val', 0) if 'valuations' in locals() else 0,
                            valuations.get('ddm_val', 0) if 'valuations' in locals() else 0,
                            valuations.get('fair_val', 0) if 'valuations' in locals() else 0,
                            valuations.get('target_price', 0) if 'valuations' in locals() else 0,
                            valuations.get('current_price', 0) if 'valuations' in locals() else 0,
                            valuations.get('upside', 0) if 'valuations' in locals() else 0
                        ]
                    }
                    summary_df = pd.DataFrame(summary_data)
                    csv_data = summary_df.to_csv(index=False)
                    
                    st.download_button(
                        label="💾 Download CSV File",
                        data=csv_data,
                        file_name=f"{ticker.replace('.NS', '')}_summary_{date.today().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                    st.success("✅ CSV summary generated successfully!")
                except Exception as e:
                    st.error(f"❌ CSV export failed: {e}")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Risk Warnings ────────────────────────────────────────────────────
    with st.expander("⚠️ Risk Warnings & Model Limitations"):
        st.markdown(create_info_card(
            "Important Investment Disclaimers",
            """
            • **Model Limitations**: DCF and DDM are simplified valuation models. Real investments involve countless variables not captured here.
            
            • **Assumption Sensitivity**: Small changes in growth rates, discount rates, or terminal values can dramatically impact results.
            
            • **Market Dynamics**: Models don't account for market sentiment, macroeconomic conditions, or black swan events.
            
            • **Data Dependencies**: Results are only as good as the underlying financial data quality and accuracy.
            
            • **Educational Purpose**: This tool is for learning and analysis only. Always consult qualified financial advisors for investment decisions.
            
            • **Past Performance**: Historical trends and data do not guarantee future performance or results.
            """,
            "warning"
        ), unsafe_allow_html=True)

    # ── Modern Footer ────────────────────────────────────────────────────
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    footer_col1, footer_col2, footer_col3 = st.columns(3)
    
    with footer_col1:
        st.markdown(f"""
        <div style="text-align: center;">
            <h4 style="color: #1f2937; margin-bottom: 0.5rem;">📊 Analysis Summary</h4>
            <p style="color: #6b7280; margin: 0;">
                {analysis_mode.replace('🎯 ', '').replace('📊 ', '').replace('🏢 ', '').replace('📋 ', '')} Analysis Complete
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with footer_col2:
        st.markdown(f"""
        <div style="text-align: center;">
            <h4 style="color: #1f2937; margin-bottom: 0.5rem;">📡 Data Source</h4>
            <p style="color: #6b7280; margin: 0;">
                {provider}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with footer_col3:
        st.markdown(f"""
        <div style="text-align: center;">
            <h4 style="color: #1f2937; margin-bottom: 0.5rem;">🕒 Last Updated</h4>
            <p style="color: #6b7280; margin: 0;">
                {datetime.now().strftime('%Y-%m-%d %H:%M IST')}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Floating Action Tips ─────────────────────────────────────────────
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 💡 Pro Tips")
        
        tips = [
            "🎯 Use **Comprehensive Report** for detailed institutional-grade analysis",
            "📊 **Scenario Analysis** helps stress-test your assumptions", 
            "🏢 **Peer Comparison** provides market context and relative valuation",
            "🌡️ **Sensitivity Analysis** shows how robust your valuation is",
            "📤 **Export Reports** for presentations and further analysis",
            "⚖️ Always combine with **fundamental analysis** and due diligence",
            "🔄 **Refresh data** regularly as markets change",
            "📚 **Cross-reference** with analyst reports and company filings"
        ]
        
        for tip in tips:
            st.markdown(f"• {tip}")
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 10px; color: white; margin-top: 1rem;">
            <h4 style="margin: 0 0 0.5rem 0;">🚀 Enhanced Features</h4>
            <p style="margin: 0; font-size: 0.9rem;">
                Built with modern UI/UX principles<br>
                Interactive charts • Real-time data • Export functionality
            </p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()