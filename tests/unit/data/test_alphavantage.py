import os
import pytest
from unittest.mock import patch, MagicMock
from datetime import date
from ivnse.data.alphavantage import AlphaVantageProvider

# Mock API response data
def mock_quote_response():
    return {
        "Global Quote": {
            "01. symbol": "INFY.NS",
            "05. price": "2,100.50",
            "06. volume": "1,000,000",
            "07. latest trading day": "2023-06-22",
            "08. previous close": "2,090.00"
        }
    }

def mock_fundamentals_response():
    return {
        "Symbol": "INFY.NS",
        "Name": "Infosys",
        "Exchange": "NSE",
        "Country": "India",
        "Sector": "Technology",
        "Industry": "Software",
        "MarketCapitalization": "100000000000",
        "PERatio": "30.5",
        "PEGRatio": "1.5",
        "BookValue": "1000.00",
        "DividendPerShare": "20.00",
        "DividendYield": "1.00",
        "EPS": "70.00",
        "RevenuePerShareTTM": "500.00",
        "ProfitMargin": "25.00",
        "OperatingMarginTTM": "30.00",
        "ReturnOnAssetsTTM": "15.00",
        "ReturnOnEquityTTM": "20.00",
        "QuarterlyRevenueGrowthYOY": "15.00",
        "QuarterlyEarningsGrowthYOY": "20.00"
    }

def mock_cashflow_response():
    return {
        "annualReports": [
            {
                "fiscalDateEnding": "2022-12-31",
                "operatingCashflow": "1000000000",
                "capitalExpenditures": "-200000000",
                "netIncome": "500000000",
                "freeCashFlow": "800000000"
            }
        ]
    }

@pytest.fixture
def provider():
    return AlphaVantageProvider()

def test_supports_nse(provider):
    assert provider.supports("INFY.NS")
    assert provider.supports("RELIANCE.NS")

def test_supports_bse(provider):
    assert provider.supports("INFY.BO")
    assert provider.supports("RELIANCE.BO")

def test_supports_global(provider):
    assert not provider.supports("AAPL")
    assert not provider.supports("MSFT")

def test_get_quote_success(provider):
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_quote_response()
        mock_get.return_value = mock_response
        
        quote = provider.get_quote("INFY.NS")
        
        assert quote["symbol"] == "INFY.NS"
        assert quote["price"] == 2100.50
        assert quote["currency"] == "INR"
        assert quote["volume"] == 1000000
        assert quote["latestDay"] == "2023-06-22"

def test_get_quote_invalid_symbol(provider):
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"Error Message": "Invalid API call."}
        mock_get.return_value = mock_response
        
        with pytest.raises(ValueError):
            provider.get_quote("INVALID.NS")

def test_get_fundamentals_success(provider):
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_fundamentals_response()
        mock_get.return_value = mock_response
        
        fundamentals = provider.get_fundamentals("INFY.NS")
        assert fundamentals["Symbol"] == "INFY.NS"
        assert fundamentals["Sector"] == "Technology"
        assert fundamentals["Country"] == "India"

def test_get_cashflows_success(provider):
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_cashflow_response()
        mock_get.return_value = mock_response
        
        cashflows = provider.get_cashflows("INFY.NS")
        assert len(cashflows) == 1
        assert cashflows[0]["fiscalDateEnding"] == "2022-12-31"
        assert cashflows[0]["operatingCashflow"] == "1000000000"

def test_throttle(provider):
    with patch('time.time') as mock_time:
        mock_time.return_value = 0
        provider._get(function="TEST", symbol="INFY.NS")
        assert provider._LAST_HIT == 0
        
        # Simulate another request within 12 seconds
        mock_time.return_value = 10
        with pytest.raises(Exception):
            provider._get(function="TEST", symbol="INFY.NS")
