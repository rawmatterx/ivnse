# Intrinsic Value Calculator Architecture

## Overview

The Intrinsic Value Calculator is a modern Streamlit-based application designed to calculate the intrinsic value of stocks using various valuation models and data providers. The application follows a modular architecture with clear separation of concerns.

## Core Components

### 1. Data Layer (`ivnse/data/`)
- **Data Providers**:
  - `alphavantage.py`: Handles NSE/BSE tickers with rate limiting
  - `fmp.py`: Primary global data provider
  - `yahoo.py`: Fallback for global data
  - `factory.py`: Provider orchestration with automatic fallbacks

- **Key Features**:
  - Multi-provider data fetching
  - Rate limiting and caching
  - Error handling and retries
  - Environment-based configuration

### 2. Model Layer (`ivnse/models/`)
- **Valuation Models**:
  - `DCF`: Discounted Cash Flow model
  - `DDM`: Dividend Discount Model
  - Financial ratio calculations

- **Settings Classes**:
  - `DCFSettings`: Configuration for DCF model
  - `DDMSettings`: Configuration for DDM model
  - `ScenarioSettings`: Parameters for scenario analysis

### 3. UI Layer (`ivnse/ui/`)
- **Components**:
  - Modern UI with glassmorphism design
  - Interactive visualizations
  - Responsive layout
  - Animated metrics and cards

- **Key Features**:
  - Streamlit-based interactive interface
  - Modern styling system
  - Reusable UI components
  - Interactive charts and graphs

### 4. Utility Layer (`ivnse/utils/`)
- **Shared Utilities**:
  - Data fetching helpers
  - Configuration management
  - Constants and enums
  - Error handling utilities

## Data Flow

1. **User Input** → Stock ticker and parameters via UI
2. **Data Fetching** → ProviderFactory selects appropriate data provider
3. **Model Processing** → Valuation models calculate intrinsic value
4. **UI Rendering** → Results displayed with interactive visualizations

## Technical Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas
- **Visualization**: Plotly
- **Data Sources**: Alpha Vantage, FMP, Yahoo Finance
- **Excel Export**: Openpyxl

## Environment Requirements

- Python ≥ 3.10
- Required API Keys:
  - ALPHAVANTAGE_API_KEY
  - FMP_API_KEY

## Development Guidelines

1. **Code Style**:
   - Follow PEP 8
   - Use type hints
   - Maintain consistent naming

2. **Testing**:
   - Unit tests for all models
   - Integration tests for data flow
   - UI component testing

3. **Documentation**:
   - Docstrings for all public functions
   - API documentation
   - Example usage

## Future Improvements

1. **Enhanced Testing**:
   - More comprehensive test coverage
   - Performance testing
   - Integration tests

2. **Additional Features**:
   - More valuation models
   - Advanced scenario analysis
   - Portfolio analysis

3. **Technical Improvements**:
   - Better caching mechanism
   - Enhanced error handling
   - Performance optimizations
