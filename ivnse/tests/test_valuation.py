from ivnse.services.valuation import discounted_cash_flow

def test_dcf_basic():
    # Simple DCF test
    result = discounted_cash_flow(100, [0.1]*10, 0.12, 0.02, 1e9)
    assert result > 0
