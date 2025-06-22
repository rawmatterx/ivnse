# Intrinsic Value Calculator

A Streamlit app to calculate the intrinsic value of stocks. Ready for local development, Docker, and Heroku deployment.

## Quickstart

```sh
# 1. Set up environment variables
# Get your free API keys from:
# - Alpha Vantage: https://www.alphavantage.co/support/#api-key
# - Financial Modeling Prep: https://financialmodelingprep.com/developer/docs/

export ALPHAVANTAGE_API_KEY=your_alpha_key
export FMP_API_KEY=your_fmp_key

# 2. Install and run
pip install -e .
streamlit run app.py
```

## Supported Exchanges

- **NSE/BSE** (India): `.NS` (NSE) or `.BO` (BSE) suffixes
  - Example: `INFY.NS` (Infosys), `RELIANCE.NS` (Reliance)
- **Global Markets**: US, UK, Canada, and more
  - Example: `AAPL` (Apple), `BP.L` (BP London), `SHOP.TO` (Shopify Toronto)

The app uses a multi-provider data layer that prioritizes:
1. Alpha Vantage (NSE/BSE & global backup)
2. Financial Modeling Prep (primary global provider)
3. Yahoo Finance (global fallback)

## Architecture

```
ivnse/
├─ ivnse/
│  ├─ data/        # Multi-provider data layer
│  │  ├─ alphavantage.py   # NSE/BSE & global backup
│  │  ├─ fmp.py          # Primary global provider
│  │  ├─ yahoo.py        # Global fallback
│  │  └─ factory.py      # Provider orchestration
│  ├─ models/
│  ├─ ui/
│  ├─ utils/
│  └─ __init__.py
├─ tests/
├─ app.py
├─ requirements.txt
├─ setup.cfg
├─ pyproject.toml
└─ docs/
```

## Contributing
See the PR template and sprint plan in the docs.
