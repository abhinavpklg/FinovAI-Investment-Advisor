# function to format large numbers
def format_large_number(num):
    if num >= 1_000_000_000_000:  # Trillions
        return f"{num / 1_000_000_000_000:.1f}T"
    elif num >= 1_000_000_000:  # Billions
        return f"{num / 1_000_000_000:.1f}B"
    elif num >= 1_000_000:  # Millions
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:  # Thousands
        return f"{num / 1_000:.1f}K"
    else:  # Less than 1,000
        return str(num)


def format_colored_number(value):
    color = (
        "green" if value >= 0 else "red"
    )  # Choose green for positive, red for negative
    return f'<div style="color:{color}; font-size:20px; font-weight:bold;">{value * 100:.1f}%</div>'  # Format number to 2 decimal places


def safe_format(value):
    # Handle invalid or missing values
    if isinstance(value, (int, float)):
        return f"{value * 100:.1f}%"
    else:
        return "N/A"


def validate_user_profile(profile):
    """
    Validates user profile data according to business rules
    """
    try:
        # Check if all required fields are present
        required_fields = ['gender', 'age', 'income', 'expenditure', 'savings', 'objective', 'duration']
        if not all(field in profile for field in required_fields):
            raise ValueError("Missing required fields")

        # Validate age (18-100)
        if not isinstance(profile['age'], (int, float)) or not (18 <= profile['age'] <= 100):
            raise ValueError("Age must be between 18 and 100")

        # Validate income and expenditure
        if not isinstance(profile['income'], (int, float)) or profile['income'] <= 0:
            raise ValueError("Income must be greater than 0")
        if not isinstance(profile['expenditure'], (int, float)) or profile['expenditure'] >= profile['income']:
            raise ValueError("Expenditure must be less than income")

        # Validate savings
        if not isinstance(profile['savings'], (int, float)) or profile['savings'] < 0:
            raise ValueError("Savings cannot be negative")

        # Validate investment duration
        if not isinstance(profile['duration'], (int, float)) or not (1 <= profile['duration'] <= 40):
            raise ValueError("Investment duration must be between 1 and 40 years")

        return True

    except (KeyError, TypeError, ValueError) as e:
        raise ValueError(str(e))


def filter_stocks(filters):
    """
    Filters stocks based on given criteria
    """
    if not isinstance(filters, dict):
        raise ValueError("Filters must be a dictionary")
        
    if filters.get('Market Cap', 0) < 0:
        raise ValueError("Market Cap must be positive")
        
    if filters.get('Volume', 0) < 0:
        raise ValueError("Volume must be positive")
        
    if not isinstance(filters.get('Recommendation Keys', []), list):
        raise ValueError("Recommendation Keys must be a list")
        
    valid_recommendations = ["strong buy", "buy", "hold", "sell", "strong sell"]
    if any(key not in valid_recommendations for key in filters.get('Recommendation Keys', [])):
        raise ValueError("Invalid recommendation key")

    # Your stock filtering logic here
    return []


def generate_recommendations(query, filters, pinecone_index=None):
    """
    Generates stock recommendations based on user query and filters
    """
    try:
        # Validate inputs
        if not query or not isinstance(query, str):
            raise ValueError("Invalid query")
        if not isinstance(filters, dict):
            raise ValueError("Invalid filters")

        # Placeholder for recommendation logic
        return {
            'recommendations': ['AAPL', 'MSFT'],
            'analysis': 'Selected based on growth potential and market position'
        }

    except Exception as e:
        raise ValueError(f"Error generating recommendations: {str(e)}")
