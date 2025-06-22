from __future__ import annotations
from typing import List, Type, TypeVar, Generic
from .base import BaseProvider
from .alphavantage import AlphaVantageProvider
from .fmp import FMPProvider
from .nsepy_provider import NSEpyProvider
from .yahoo import YahooProvider

T = TypeVar('T', bound=BaseProvider)

class ProviderFactory(Generic[T]):
    """Factory for creating data providers with fallbacks."""
    
    _PROVIDERS: List[Type[T]] = [
        NSEpyProvider,        # Primary NSE provider
        AlphaVantageProvider, # Fallback for BSE/global
        FMPProvider,          # Fallback for global
        YahooProvider,        # Last resort fallback
    ]

    @classmethod
    def get_provider(cls, symbol: str) -> T:
        """Get a provider that supports the given symbol."""
        for Provider in cls._PROVIDERS:
            if Provider.supports(symbol):
                return Provider()
        raise ValueError(f"No provider supports symbol: {symbol}")

    @classmethod
    def get_quote(cls, symbol: str) -> Dict[str, Any]:
        """Get quote data with automatic provider fallback."""
        provider = cls.get_provider(symbol)
        return provider.get_quote(symbol)

    @classmethod
    def get_fundamentals(cls, symbol: str) -> Dict[str, Any]:
        """Get fundamentals data with automatic provider fallback."""
        provider = cls.get_provider(symbol)
        return provider.get_fundamentals(symbol)

    @classmethod
    def get_cashflows(cls, symbol: str, as_of: date | None = None) -> List[Dict[str, Any]]:
        """Get cashflow data with automatic provider fallback."""
        provider = cls.get_provider(symbol)
        return provider.get_cashflows(symbol, as_of)
