from main import Product
from dataclasses import is_dataclass
import pytest

@pytest.fixture
def product():
    return Product(1, 'foo', 1.0, 10)

def test_constructor(product):
    assert product.id == 1
    assert product.name == 'foo'
    assert product.price == 1.0
    assert product.stock == 10

def test_is_dataclass():
    assert is_dataclass(Product)

def test_increase_stock(product):
    original_stock = product.stock
    product.increase_stock(5)
    assert product.stock == original_stock + 5

def test_decrease_stock(product):
    original_stock = product.stock
    product.decrease_stock(3)
    assert product.stock == original_stock - 3

def test_increase_stock_with_non_positive_number(product):
    with pytest.raises(Exception, match="Number must be positive"):
        product.increase_stock(-1)

def test_decrease_stock_with_non_positive_number(product):
    with pytest.raises(Exception, match="Number must be positive"):
        product.decrease_stock(0)

def test_decrease_stock_below_zero(product):
    with pytest.raises(Exception, match="Stock must be greater than or equal to 0"):
        product.decrease_stock(product.stock + 1)

##This set of tests ensures various functionalitof the `Product` class, including the constructor, stock increase and decrease operations, and exception handling for improper inp