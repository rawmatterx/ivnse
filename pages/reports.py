import streamlit as st
import pandas as pd
from datetime import date
from ivnse.core import create_info_card

st.title("Reports & Export")
st.markdown("Download Excel/CSV, view historical valuations, and more.")

# Dummy historical data for demo
historical = pd.DataFrame({
    "Date": pd.date_range(end=date.today(), periods=10),
    "DCF Value": [100 + i*5 for i in range(10)],
    "DDM Value": [90 + i*4 for i in range(10)],
    "Fair Value": [95 + i*4.5 for i in range(10)]
})

st.dataframe(historical, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    csv = historical.to_csv(index=False)
    st.download_button("Download CSV", csv, file_name="historical_valuations.csv", mime="text/csv")
with col2:
    excel = historical.to_excel(index=False)
    st.download_button("Download Excel", excel, file_name="historical_valuations.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

st.markdown(create_info_card("Note", "Exported data is for demonstration. Integrate with real valuation history for production use."), unsafe_allow_html=True)
