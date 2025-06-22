"""NSEpy data provider implementation."""

from __future__ import annotations
from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional
import logging

import pandas as pd
from nsepy import get_history, get_quote, get_fno_quote
from nsepy.derivatives import get_expiry_date

from .base import BaseProvider

log = logging.getLogger(__name__)

class NSEpyProvider(BaseProvider):
    """Data provider for NSE (National Stock Exchange of India) using NSEpy."""
    
    def supports(self, symbol: str) -> bool:
        """Check if this provider supports the given symbol.
        
        Args:
            symbol: Stock ticker symbol (without .NS suffix)
            
        Returns:
            bool: True if provider supports the symbol (all NSE symbols supported)
        """
        # NSEpy works with NSE symbols directly, no .NS suffix needed
        return not any(symbol.endswith(suffix) for suffix in ('.NS', '.BO'))
    
    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """Get real-time quote data for a symbol.
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            dict: Quote data including price, volume, etc.
            
        Raises:
            ValueError: If quote data cannot be retrieved
        """
        try:
            # Remove .NS suffix if present
            clean_symbol = symbol.replace('.NS', '')
            quote = get_quote(clean_symbol)
            
            # Convert to standard format
            return {
                'symbol': f"{clean_symbol}.NS",
                'price': float(quote['lastPrice'].replace(',', '')),
                'change': float(quote['change'].replace(',', '')),
                'change_percent': float(quote['pChange']),
                'open': float(quote['open'].replace(',', '')),
                'high': float(quote['intraDayHighLow'].split(' - ')[0].replace(',', '')),
                'low': float(quote['intraDayHighLow'].split(' - ')[1].replace(',', '')),
                'previous_close': float(quote['previousClose'].replace(',', '')),
                'volume': int(quote['totalTradedVolume'].replace(',', '')),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            log.error(f"Error fetching quote for {symbol}: {str(e)}")
            raise ValueError(f"Could not fetch quote for {symbol}") from e
    
    def get_fundamentals(self, symbol: str) -> Dict[str, Any]:
        """Get fundamental data for a symbol.
        
        Note: NSEpy has limited fundamental data. Consider using another provider
        for comprehensive fundamental data.
        """
        # NSEpy has limited fundamental data capabilities
        # We'll return basic info from the quote for now
        try:
            quote = self.get_quote(symbol)
            return {
                'companyName': symbol.replace('.NS', ''),
                'marketCap': None,  # Not directly available
                'sector': 'N/A',
                'industry': 'N/A',
                'currentPrice': quote['price'],
                'previousClose': quote['previous_close'],
                'volume': quote['volume'],
                'currency': 'INR',
                'exchange': 'NSE',
                'quoteType': 'EQUITY'
            }
        except Exception as e:
            log.error(f"Error fetching fundamentals for {symbol}: {str(e)}")
            return {}
    
    def get_cashflows(self, symbol: str, as_of: Optional[date] = None) -> List[Dict[str, Any]]:
        """Get historical cash flow data.
        
        Note: NSEpy doesn't provide direct cash flow data.
        This is a placeholder that returns an empty list.
        """
        return []
    
    def get_income_statement(self, symbol: str) -> Dict[str, Any]:
        """Get income statement data.
        
        Note: NSEpy doesn't provide direct income statement data.
        This is a placeholder that returns an empty dict.
        """
        return {}
    
    def get_balance_sheet(self, symbol: str) -> Dict[str, Any]:
        """Get balance sheet data.
        
        Note: NSEpy doesn't provide direct balance sheet data.
        This is a placeholder that returns an empty dict.
        """
        return {}
    
    def get_dividends(self, symbol: str) -> List[Dict[str, Any]]:
        """Get dividend history.
        
        Note: NSEpy doesn't provide direct dividend history.
        This is a placeholder that returns an empty list.
        """
        return []
    
    def get_company_profile(self, symbol: str) -> Dict[str, Any]:
        """Get company profile information.
        
        Returns basic company information from the quote.
        """
        quote = self.get_quote(symbol)
        return {
            'symbol': quote['symbol'],
            'name': symbol.replace('.NS', ''),
            'exchange': 'NSE',
            'currency': 'INR',
            'marketState': 'REGULAR',
            'quoteType': 'EQUITY',
            'sharesOutstanding': None,
            'bookValue': None,
            'priceToBook': None,
            'trailingPE': None,
            'forwardPE': None,
            'dividendYield': None,
            'payoutRatio': None,
            'beta': None,
            'fiftyTwoWeekHigh': None,
            'fiftyTwoWeekLow': None
        }
