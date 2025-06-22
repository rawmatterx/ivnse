import httpx
import streamlit as st

@st.cache_data(ttl=3600)
async def fetch_fmp(endpoint, params, api_key):
    url = f"https://financialmodelingprep.com/api/v3/{endpoint}"
    headers = {"User-Agent": "ivnse/1.0"}
    params["apikey"] = api_key
    async with httpx.AsyncClient() as client:
        r = await client.get(url, params=params, headers=headers, timeout=15)
        r.raise_for_status()
        return r.json()
