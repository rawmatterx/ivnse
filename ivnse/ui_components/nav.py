import streamlit as st

def main_nav():
    st.markdown('''
    <nav style="display:flex;align-items:center;justify-content:space-between;padding:0.5rem 1rem;background:rgba(255,255,255,0.7);backdrop-filter:blur(10px);border-radius:16px;margin-bottom:1.5rem;">
        <div style="display:flex;align-items:center;gap:1rem;">
            <img src="/app/static/logo.svg" alt="ivnse" style="height:2.2rem;vertical-align:middle;">
            <span style="font-size:1.5rem;font-weight:700;color:#4F46E5;">ivnse</span>
        </div>
        <div style="display:flex;gap:1.5rem;font-size:1.1rem;">
            <a href="/" style="color:#4F46E5;text-decoration:none;font-weight:600;">Dashboard</a>
            <a href="/valuation" style="color:#4F46E5;text-decoration:none;font-weight:600;">Valuation</a>
            <a href="/peers" style="color:#4F46E5;text-decoration:none;font-weight:600;">Peers</a>
            <a href="/scenario_lab" style="color:#4F46E5;text-decoration:none;font-weight:600;">Scenario Lab</a>
            <a href="/reports" style="color:#4F46E5;text-decoration:none;font-weight:600;">Reports</a>
        </div>
        <div>
            <button onclick="window.location.reload()" style="background:#06B6D4;color:white;border:none;border-radius:8px;padding:0.5rem 1.2rem;font-weight:600;cursor:pointer;">Refresh</button>
        </div>
    </nav>
    ''', unsafe_allow_html=True)
