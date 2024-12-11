import pytest
from unittest.mock import Mock, patch
import pandas as pd
import os
import sys
from dotenv import load_dotenv

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.utils import validate_user_profile, filter_stocks, generate_recommendations

# ---- Fixtures ----
@pytest.fixture
def mock_stock_data():
    """Mock stock data for testing"""
    return {
        'AAPL': {
            'marketCap': 3000000000,
            'volume': 50000,
            'recommendation': 'buy',
            'description': 'Technology company focused on consumer electronics'
        },
        'TSLA': {
            'marketCap': 2000000000,
            'volume': 40000,
            'recommendation': 'hold',
            'description': 'Electric vehicle and clean energy company'
        }
    }

@pytest.fixture
def sample_user_profile():
    """Sample user profile for testing"""
    return {
        "gender": "Male",
        "age": 30,
        "income": 8000,
        "expenditure": 5000,
        "savings": 50000,
        "objective": "Growth",
        "duration": 10
    }

@pytest.fixture
def mock_pinecone_index():
    return Mock()

# ---- Test Cases ----

# 1. Test Stock Analysis Functions
def test_stock_filtering(mock_stock_data):
    """Test stock filtering based on user criteria"""
    filters = {
        'Market Cap': 1000000000,
        'Volume': 30000,
        'Recommendation Keys': ['buy', 'hold']
    }
    
    with patch('yfinance.Ticker') as mock_ticker:
        mock_ticker.return_value.info = mock_stock_data
        filtered_stocks = filter_stocks(filters)
        
        assert isinstance(filtered_stocks, list)
        if filtered_stocks:  # If any stocks match the criteria
            for stock in filtered_stocks:
                assert stock['volume'] >= filters['Volume']
                assert stock['marketCap'] >= filters['Market Cap']
                assert stock['recommendation'] in filters['Recommendation Keys']

# 2. Test User Profile Validation
def test_user_profile_validation(sample_user_profile):
    """Test user profile input validation"""
    # Test valid profile
    assert validate_user_profile(sample_user_profile) == True
    
    # Test invalid profile
    invalid_profile = {
        'gender': 'Male',
        'age': -1,  # Invalid age
        'income': 'invalid'  # Invalid income type
    }
    with pytest.raises(ValueError):
        validate_user_profile(invalid_profile)

# 3. Test Stock Recommendation Generation
def test_stock_recommendations(mock_pinecone_index):
    """Test stock recommendation generation"""
    user_query = "Looking for high-growth tech stocks"
    filters = {
        'Market Cap': 1000000000,
        'Volume': 30000,
        'Recommendation Keys': ['strong buy', 'buy']
    }
    
    with patch('utils.utils.generate_recommendations') as mock_recommend:
        expected_result = {
            'recommendations': ['AAPL', 'MSFT'],
            'analysis': 'Selected based on growth potential and market position'
        }
        mock_recommend.return_value = expected_result
        
        result = generate_recommendations(user_query, filters, mock_pinecone_index)
        assert isinstance(result, dict)
        assert 'recommendations' in result
        assert 'analysis' in result
        assert len(result['recommendations']) > 0

# 4. Test Error Handling
def test_error_handling():
    """Test error handling in main functions"""
    # Test invalid filters
    with pytest.raises(ValueError):
        invalid_filters = {
            'Market Cap': -1000,
            'Volume': 30000,
            'Recommendation Keys': ['invalid_key']
        }
        filter_stocks(invalid_filters)
    
    # Test invalid profile
    with pytest.raises(ValueError):
        invalid_profile = {
            'gender': None,
            'age': 'invalid',
            'income': -1000
        }
        validate_user_profile(invalid_profile)

if __name__ == '__main__':
    pytest.main(['-v']) 