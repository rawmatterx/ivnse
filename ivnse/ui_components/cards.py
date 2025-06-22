import streamlit as st

def glass_card(content, width="100%"):
    st.markdown(
        f'''
        <div class="glass-card" style="width:{width};">
            {content}
        </div>
        ''',
        unsafe_allow_html=True
    )

def metric_card(label, value, delta=None):
    st.markdown(
        f"""
        <div class="glass-card modern-metric">
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
            {'<div class="status-positive">' + delta + '</div>' if delta else ''}
        </div>
        """,
        unsafe_allow_html=True
    )
