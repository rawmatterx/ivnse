import os, pytest
from ivnse.data.alphavantage import AlphaVantageProvider

@pytest.mark.skipif("ALPHAVANTAGE_API_KEY" not in os.environ,
                    reason="Alpha Vantage key missing")
def test_quote_infys():
    p = AlphaVantageProvider()
    q = p.get_quote("INFY.NS")
    assert q["currency"] == "INR" and q["price"] > 0
