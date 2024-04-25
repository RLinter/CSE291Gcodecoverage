
from main import Product
from dataclasses import is_dataclass
import pytest


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

