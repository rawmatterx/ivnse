# Developer Guide

## Getting Started

### Prerequisites

1. Python ≥ 3.10
2. Git
3. Poetry (for dependency management)
4. Required API Keys:
   - ALPHAVANTAGE_API_KEY
   - FMP_API_KEY

### Installation

1. Clone the repository:
```bash
git clone https://github.com/rawmatterx/ivnse.git
cd ivnse
```

2. Install dependencies:
```bash
poetry install
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. Run the application:
```bash
poetry run streamlit run app.py
```

## Project Structure

```
ivnse/
├── data/           # Data providers and API integrations
│   ├── alphavantage.py
│   ├── fmp.py
│   ├── yahoo.py
│   └── factory.py
├── models/        # Valuation models and calculations
│   ├── dcf.py
│   ├── ddm.py
│   └── ratios.py
├── ui/            # Streamlit UI components
│   ├── components.py
│   ├── styling.py
│   └── charts.py
├── utils/         # Shared utilities
│   ├── data.py
│   ├── config.py
│   └── constants.py
└── main.py        # Main entry point
```

## Development Workflow

### 1. Code Style

- Follow PEP 8 style guide
- Use type hints
- Include docstrings for all public functions
- Use meaningful variable names
- Keep functions focused and small

### 2. Testing

1. Unit Tests:
```bash
poetry run pytest tests/unit/
```

2. Integration Tests:
```bash
poetry run pytest tests/integration/
```

3. Test Coverage:
```bash
poetry run pytest --cov=ivnse tests/
```

### 3. Code Formatting

1. Black:
```bash
poetry run black .
```

2. Isort:
```bash
poetry run isort .
```

### 4. Type Checking

```bash
poetry run pyright .
```

## Adding New Features

### 1. Data Provider

1. Create new provider class in `data/`
2. Implement required methods:
   - `supports()`
   - `get_quote()`
   - `get_fundamentals()`
   - `get_cashflows()`
3. Add to `ProviderFactory._PROVIDERS`
4. Add tests in `tests/test_data/`

### 2. Valuation Model

1. Create new model in `models/`
2. Add configuration class
3. Implement calculation logic
4. Add tests in `tests/test_models/`

### 3. UI Component

1. Create new component in `ui/`
2. Follow existing styling patterns
3. Make responsive
4. Add tests in `tests/test_ui/`

## Best Practices

1. **Error Handling**:
   - Use specific exceptions
   - Include helpful error messages
   - Handle API rate limits

2. **Performance**:
   - Use caching where appropriate
   - Optimize data fetching
   - Minimize API calls

3. **Documentation**:
   - Document all public functions
   - Include examples
   - Update README.md

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Format code
6. Create PR with description

## Common Tasks

### Run Application
```bash
poetry run streamlit run app.py
```

### Run Tests
```bash
poetry run pytest
```

### Format Code
```bash
poetry run black .
poetry run isort .
```

### Check Type Safety
```bash
poetry run pyright .
```

### Generate Documentation
```bash
# Coming soon
```

## Troubleshooting

### Common Issues

1. **API Key Errors**:
   - Check environment variables
   - Verify API key format
   - Check rate limits

2. **Data Fetching Issues**:
   - Check network connection
   - Verify API endpoints
   - Check error logs

3. **UI Issues**:
   - Check browser console
   - Verify Streamlit version
   - Check CSS conflicts
