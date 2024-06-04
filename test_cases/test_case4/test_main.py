import pytest
import main

# Generate test cases programmatically
@pytest.mark.parametrize("i", range(1, 1001))
def test_dynamic_variable_value(i):
    var_name = f"var{i}"
    expected_value = i
    
    # Check if the variable exists in the module
    assert hasattr(main, var_name), f"{var_name} does not exist"
    
    # Retrieve the variable's value from the module
    var_value = getattr(main, var_name)
    
    # Check if the variable's value is what we expect
    assert var_value == expected_value, f"{var_name} should be {expected_value} but is {var_value}"
