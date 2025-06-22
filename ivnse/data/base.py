"""Base interface for data providers.

This module defines the common interface that all data providers must implement.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

class BaseProvider(ABC):
    """Abstract base class for data providers.
    
    All data providers must implement this interface.
    """
    
    @abstractmethod
    def supports(self, symbol: str) -> bool:
        """Check if this provider supports the given symbol.
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            bool: True if provider supports the symbol, False otherwise
        """
        pass
    
    @abstractmethod
    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """Get real-time quote data for a symbol.
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            dict: Quote data including price, volume, etc.
            
        Raises:
            ValueError: If quote data cannot be retrieved
        """
        pass
    
    @abstractmethod
    def get_fundamentals(self, symbol: str) -> Dict[str, Any]:
        """Get fundamental data for a symbol.
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            dict: Fundamental data including financial metrics
            
        Raises:
            ValueError: If fundamental data cannot be retrieved
        """
        pass
    
    @abstractmethod
    def get_cashflows(self, symbol: str, as_of: Optional[date] = None) -> List[Dict[str, Any]]:
        """Get cashflow statements for a symbol.
        
        Args:
            symbol: Stock ticker symbol
            as_of: Date to get cashflows for (optional)
            
        Returns:
            list: List of cashflow statements
            
        Raises:
            ValueError: If cashflow data cannot be retrieved
        """
        pass
    
    @abstractmethod
    def get_dividends(self, symbol: str) -> List[Dict[str, Any]]:
        """Get dividend history for a symbol.
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            list: List of dividend payments
            
        Raises:
            ValueError: If dividend data cannot be retrieved
        """
        pass
    
    @abstractmethod
    def get_income_statement(self, symbol: str) -> Dict[str, Any]:
        """Get income statement data for a symbol.
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            dict: Income statement data
            
        Raises:
            ValueError: If income statement cannot be retrieved
        """
        pass
    
    @abstractmethod
    def get_balance_sheet(self, symbol: str) -> Dict[str, Any]:
        """Get balance sheet data for a symbol.
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            dict: Balance sheet data
            
        Raises:
            ValueError: If balance sheet cannot be retrieved
        """
        pass
    
    @abstractmethod
    def get_company_profile(self, symbol: str) -> Dict[str, Any]:
        """Get company profile information.
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            dict: Company profile data including name, sector, etc.
            
        Raises:
            ValueError: If company profile cannot be retrieved
        """
        pass
