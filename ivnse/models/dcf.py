"""Discounted Cash Flow (DCF) valuation model implementation.

This module provides the core functionality for calculating the intrinsic value
of a company using the Discounted Cash Flow method.
"""

from __future__ import annotations
import math
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@dataclass
class DCFSettings:
    """Settings for the Discounted Cash Flow model.
    
    Attributes:
        growth_rates: List of growth rates for each year
        discount_rate: Required rate of return (WACC)
        terminal_growth: Long-term growth rate after projection period
        shares_outstanding: Number of shares outstanding (used for per-share calculations)
    """
    growth_rates: List[Union[float, Decimal]]
    discount_rate: Union[float, Decimal]
    terminal_growth: Union[float, Decimal]
    shares_outstanding: float
    
    def validate(self) -> None:
        """Validate the settings values."""
        if not self.growth_rates or len(self.growth_rates) < 1:
            raise ValueError("At least one growth rate must be provided")
            
        if self.discount_rate <= 0 or self.discount_rate >= 1:
            raise ValueError("Discount rate must be between 0 and 1")
            
        if self.terminal_growth < 0 or self.terminal_growth >= self.discount_rate:
            raise ValueError("Terminal growth rate must be non-negative and less than discount rate")
            
        if self.shares_outstanding <= 0:
            raise ValueError("Shares outstanding must be positive")

    def calculate_terminal_value(self, final_cash_flow: Decimal) -> Decimal:
        """Calculate terminal value using Gordon Growth Model with adjusted discounting.
        
        Args:
            final_cash_flow: Last projected cash flow
            
        Returns:
            Decimal: Terminal value
        """
        terminal_growth = Decimal(str(self.terminal_growth))
        discount_rate = Decimal(str(self.discount_rate))
        
        # Apply more aggressive discounting to terminal value
        discount_factor = (1 + discount_rate) ** 7  # Additional 7-year discount
        
        # Apply safety margin (reduce terminal value by 20%)
        safety_margin = Decimal('0.80')
        
        return (final_cash_flow * (1 + terminal_growth) / 
                (discount_rate - terminal_growth)) / discount_factor * safety_margin

def discounted_cash_flow(
    last_owner_earnings: Union[float, Decimal],
    settings: DCFSettings,
    years: int = 10,
    precision: int = 2
) -> float:
    """Calculate the intrinsic value using Discounted Cash Flow method.
    
    Args:
        last_owner_earnings: Last year's owner earnings
        settings: DCF settings including growth rates and discount rate
        years: Number of years to project (default: 10)
        precision: Decimal places for rounding (default: 2)
        
    Returns:
        float: Calculated intrinsic value
        
    Raises:
        ValueError: If input values are invalid
    """
    # Validate inputs
    if last_owner_earnings <= 0:
        raise ValueError("Owner earnings must be positive")
        
    settings.validate()
    
    # Convert inputs to Decimal for precise calculations
    if isinstance(last_owner_earnings, (int, float)):
        last_owner_earnings = Decimal(str(last_owner_earnings))
    
    # Calculate projected cash flows
    cash_flows = []
    current_earnings = last_owner_earnings
    
    logger.debug(f"Initial owner earnings: {last_owner_earnings}")
    logger.debug(f"Growth rates: {settings.growth_rates}")
    logger.debug(f"Discount rate: {settings.discount_rate}")
    logger.debug(f"Terminal growth: {settings.terminal_growth}")
    logger.debug(f"Shares outstanding: {settings.shares_outstanding}")
    
    # Project growth for each year
    for year in range(years):
        if year < len(settings.growth_rates):
            growth_rate = Decimal(str(settings.growth_rates[year]))
        else:
            if settings.growth_rates[-1] < 0:
                growth_rate = Decimal('0')  # Stabilize at 0% growth for negative growth scenarios
            else:
                growth_rate = Decimal(str(settings.growth_rates[-1]))
                
        current_earnings = current_earnings * (1 + growth_rate)
        cash_flows.append(current_earnings)
        logger.debug(f"Year {year + 1} earnings: {current_earnings}")
    
    # Calculate present value of cash flows with more aggressive discounting
    discount_rate = Decimal(str(settings.discount_rate))
    present_value = sum(
        cash_flow / (1 + discount_rate) ** (year + 1)
        for year, cash_flow in enumerate(cash_flows)
    )
    
    logger.debug(f"Present value of cash flows: {present_value}")
    
    # Calculate terminal value
    terminal_value = settings.calculate_terminal_value(cash_flows[-1])
    
    logger.debug(f"Terminal value: {terminal_value}")
    
    # Add terminal value and discount back to present
    present_value = present_value + terminal_value / (1 + discount_rate) ** years
    
    logger.debug(f"Total present value (with terminal): {present_value}")
    
    # Apply a safety margin to the final value (reduce by 15%)
    safety_margin = Decimal('0.85')
    present_value = present_value * safety_margin
    
    logger.debug(f"Final value after safety margin: {present_value}")
    
    # Round to specified precision
    final_value = float(present_value.quantize(
        Decimal('1.' + '0' * precision),
        rounding=ROUND_HALF_UP
    ))
    
    logger.debug(f"Final rounded value: {final_value}")
    
    return final_value

def calculate_growth_rate(
    current_value: float,
    future_value: float,
    periods: int
) -> float:
    """Calculate compound annual growth rate.
    
    Args:
        current_value: Starting value
        future_value: Ending value
        periods: Number of periods
        
    Returns:
        float: Compound annual growth rate
    """
    if current_value <= 0 or future_value <= 0 or periods <= 0:
        raise ValueError("Values must be positive and periods must be greater than 0")
        
    return (future_value / current_value) ** (1 / periods) - 1

def calculate_terminal_value(
    final_cash_flow: float,
    growth_rate: float,
    discount_rate: float
) -> float:
    """Calculate terminal value using Gordon Growth Model.
    
    Args:
        final_cash_flow: Last projected cash flow
        growth_rate: Terminal growth rate
        discount_rate: Required rate of return
        
    Returns:
        float: Terminal value
    """
    if growth_rate >= discount_rate:
        raise ValueError("Growth rate cannot be greater than or equal to discount rate")
        
    return final_cash_flow * (1 + growth_rate) / (discount_rate - growth_rate)

def calculate_growth_rate(
    current_value: float,
    future_value: float,
    periods: int
) -> float:
    """Calculate compound annual growth rate.
    
    Args:
        current_value: Starting value
        future_value: Ending value
        periods: Number of periods
        
    Returns:
        float: Compound annual growth rate
    """
    if current_value <= 0 or future_value <= 0 or periods <= 0:
        raise ValueError("Values must be positive and periods must be greater than 0")
        
    return (future_value / current_value) ** (1 / periods) - 1
