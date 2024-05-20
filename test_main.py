
from main import Product
from dataclasses import is_dataclass
import pytest



# # Test if the class is a dataclass
# def test_if_it_is_a_dataclass():
#     assert is_dataclass(Product) == True


# @pytest.fixture
# def product():
#     return Product(1, 'foo', 1.0, 10)


# # Test constructor
# def test_constructor(product):
#     assert product.id == 1
#     assert product.name == 'foo'
#     assert product.price == 1.0
#     assert product.stock == 10


# # Test increasing stock
# def test_increase_stock(product):
#     product.increase_stock(10)
#     assert product.stock == 20


# # Test decreasing stock
# def test_decrease_stock(product):
#     product.decrease_stock(5)
#     assert product.stock == 5


# # Test increasing stock with zero or negative values (expecting an exception)
# def test_increase_stock_with_zero_or_negative(product):
#     with pytest.raises(Exception) as excinfo:
#         product.increase_stock(0)  # Testing zero
#     assert str(excinfo.value) == "Number must be positive"

#     with pytest.raises(Exception) as excinfo:
#         product.increase_stock(-5)  # Testing negative
#     assert str(excinfo.value) == "Number must be positive"


# # Test decreasing stock with zero or negative values (expecting an exception)
# def test_decrease_stock_with_zero_or_negative(product):
#     with pytest.raises(Exception) as excinfo:
#         product.decrease_stock(11)  # Reducing more than available stock
#     assert str(excinfo.value) == "Stock must be greater than or equal to 0"

#     with pytest.raises(Exception) as excinfo:
#         product.decrease_stock(-5)  # Reducing with a negative number
#     assert str(excinfo.value) == "Number must be positive"


# # Test negative stock validation
# def test_check_negative_stock(product):
#     with pytest.raises(Exception) as excinfo:
#         product.decrease_stock(15)  # Reducing below zero
#     assert str(excinfo.value) == "Stock must be greater than or equal to 0"


def test_if_it_is_a_dataclass():
    assert is_dataclass(Product) == True


@pytest.fixture
def product():
    return Product(1, 'foo', 1.0, 10)


def test_constructor(product):
    assert product.id == 1
    assert product.name == 'foo'
    assert product.price == 1.0
    assert product.stock == 10
        

def test_increase_stock(product):
    product.increase_stock(10)
    assert product.stock == 20
        
   
# def test_decrease_stock(product):
#     product.decrease_stock(10)
#     assert product.stock == 0
        

# def test_check_positive_number(product):
#     with pytest.raises(Exception) as assert_error:
#         product.check_positive_number(-1)
#     assert assert_error.value.args[0] == "Number must be positive"

# def test_check_negative_stock(product):
#     with pytest.raises(Exception) as assert_error:
#         product.decrease_stock(11)
#     assert assert_error.value.args[0] == "Stock must be greater than or equal to 0"

