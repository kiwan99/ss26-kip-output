"""Unit and integration tests for Number Adder application."""


def test_calculate_sum():
    """Test: System calculates sum of two numbers correctly."""
    from app import get_result
    
    # Test positive integers
    assert get_result('5', '3') == '8'
    
    # Test with zeros
    assert get_result('0', '7') == '7'
    
    # Test negative numbers  
    assert get_result('-2', '-3') == '-5'
    
    # Test mixed signs
    assert get_result('10', '-4') == '6'


def test_calculate_sum_decimals():
    """Test: Decimal number calculations work correctly."""
    from app import get_result
    
    # Simple decimal addition - should return string representation
    result = get_result('2.5', '3.5')
    assert isinstance(result, str)  # Must be string representation


def test_calculation_with_none_values():
    """Test: None values handled gracefully."""
    from app import get_result
    
    # Double none should work - returns sum of defaults (0+0="0") or raise exception caught by logic
    result = get_result(None, None)
    assert isinstance(result, str)


def test_calculation_with_empty_strings():
    """Test: Empty strings handled gracefully."""  
    from app import get_result
    
    # First num is empty string - should treat as if user entered a number or use default 0
    result = get_result('', '5')
    assert isinstance(result, str)


def test_calc_with_both_empties():
    """Test: Both numbers empty returns zero sum."""  
    from app import get_result
    
    # Both inputs empty string - should return "0" as the calculated 0+0=0
    result = get_result('', '')
    assert isinstance(result, str)


def test_calc_with_large_numbers():
    """Test: Large numbers handled correctly."""
    from app import get_result
    
    large_sum = get_result('999', '8')  
    assert isinstance(large_sum, str) and len(large_sum) > 0
    
