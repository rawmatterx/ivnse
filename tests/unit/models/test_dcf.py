import pytest
from decimal import Decimal
from ivnse.models import DCFSettings, discounted_cash_flow

def test_dcf_settings_creation():
    settings = DCFSettings(
        growth_rates=[0.1, 0.08, 0.05],
        discount_rate=0.12,
        terminal_growth=0.02,
        shares_outstanding=1000000
    )
    
    assert settings.growth_rates == [0.1, 0.08, 0.05]
    assert settings.discount_rate == 0.12
    assert settings.terminal_growth == 0.02
    assert settings.shares_outstanding == 1000000

def test_dcf_calculation():
    # Test with typical growth rates and discount rate
    settings = DCFSettings(
        growth_rates=[0.1, 0.08, 0.05],
        discount_rate=0.12,
        terminal_growth=0.02,
        shares_outstanding=1000000
    )
    
    # Test with owner earnings of $1000
    dcf_value = discounted_cash_flow(1000, settings)
    
    # Expected value should be close to $10000 (rounded)
    assert round(dcf_value, 2) == 10000.00

def test_dcf_with_negative_growth():
    settings = DCFSettings(
        growth_rates=[-0.1, -0.05, 0.0],
        discount_rate=0.12,
        terminal_growth=0.02,
        shares_outstanding=1000000
    )
    
    dcf_value = discounted_cash_flow(1000, settings)
    assert dcf_value < 1000  # Should be less than initial value with negative growth

def test_dcf_with_high_discount_rate():
    settings = DCFSettings(
        growth_rates=[0.1, 0.08, 0.05],
        discount_rate=0.20,
        terminal_growth=0.02,
        shares_outstanding=1000000
    )
    
    dcf_value = discounted_cash_flow(1000, settings)
    assert dcf_value < 10000  # Higher discount rate should reduce value

def test_dcf_with_zero_growth():
    settings = DCFSettings(
        growth_rates=[0.0, 0.0, 0.0],
        discount_rate=0.12,
        terminal_growth=0.0,
        shares_outstanding=1000000
    )
    
    dcf_value = discounted_cash_flow(1000, settings)
    assert dcf_value > 0  # Should still have some value even with no growth

def test_dcf_with_high_terminal_growth():
    settings = DCFSettings(
        growth_rates=[0.1, 0.08, 0.05],
        discount_rate=0.12,
        terminal_growth=0.10,
        shares_outstanding=1000000
    )
    
    dcf_value = discounted_cash_flow(1000, settings)
    assert dcf_value > 10000  # Higher terminal growth should increase value

def test_dcf_with_invalid_input():
    settings = DCFSettings(
        growth_rates=[0.1, 0.08, 0.05],
        discount_rate=0.12,
        terminal_growth=0.02,
        shares_outstanding=1000000
    )
    
    with pytest.raises(ValueError):
        discounted_cash_flow(-1000, settings)  # Negative owner earnings

def test_dcf_with_large_numbers():
    settings = DCFSettings(
        growth_rates=[0.1, 0.08, 0.05],
        discount_rate=0.12,
        terminal_growth=0.02,
        shares_outstanding=1000000000  # 1 billion
    )
    
    dcf_value = discounted_cash_flow(10000000, settings)  # 10 million
    assert dcf_value > 100000000  # Should be greater than 100 million

def test_dcf_with_decimal_input():
    settings = DCFSettings(
        growth_rates=[Decimal('0.1'), Decimal('0.08'), Decimal('0.05')],
        discount_rate=Decimal('0.12'),
        terminal_growth=Decimal('0.02'),
        shares_outstanding=1000000
    )
    
    dcf_value = discounted_cash_flow(Decimal('1000'), settings)
    assert isinstance(dcf_value, float)
    assert round(dcf_value, 2) == 10000.00
