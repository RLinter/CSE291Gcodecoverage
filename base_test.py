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

def test_increase_stock(product):
    product.increase_stock(5)
    assert product.stock == 15

def test_decrease_stock(product):
    product.decrease_stock(5)
    assert product.stock == 5

def test_decrease_stock_exception(product):
    with pytest.raises(Exception, match="Stock must be greater than or equal to 0"):
        product.decrease_stock(20)

def test_increase_stock_with_zero(product):
    with pytest.raises(Exception, match="Number must be positive"):
        product.increase_stock(0)

def test_increase_stock_with_negative_number(product):
    with pytest.raises(Exception, match="Number must be positive"):
        product.increase_stock(-5)

def test_decrease_stock_with_zero(product):
    with pytest.raises(Exception, match="Number must be positive"):
        product.decrease_stock(0)

def test_decrease_stock_with_negative_number(product):
    with pytest.raises(Exception, match="Number must be positive"):
        product.decrease_stock(-5)
