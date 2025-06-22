"""Streamlit Intrinsic Value Calculator — Modern UI Edition v0.4

New in v0.4:
• Beautiful modern UI with glassmorphism design
• Animated metrics and progress indicators
• Enhanced color schemes and typography
• Interactive dashboard layout
• Modern card-based components
• Responsive design elements

> Setup

1. pip install -r requirements.txt
2. Grab a free key at https://financialmodelingprep.com
3. export FMP_API_KEY="YOUR_KEY" (or add to Streamlit Secrets)
4. streamlit run app.py
"""

import streamlit as st
from ivnse import app as ivnse_app

ivnse_app.main()