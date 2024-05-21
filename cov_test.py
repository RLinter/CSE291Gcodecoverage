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
def test_decrease_stock(product):
    product.decrease_stock(5)
    assert product.stock == 5

    product.decrease_stock(1)
    assert product.stock == 4

def test_decrease_stock_too_much(product):
    with pytest.raises(Exception, match="Stock must be greater than or equal to 0"):
        product.decrease_stock(11)

def test_decrease_stock_negative_value(product):
    with pytest.raises(Exception, match="Number must be positive"):
        product.decrease_stock(-5)

def test_check_positive_number_negative_value(product):
    with pytest.raises(Exception, match="Number must be positive"):
        product.check_positive_number(-1)

def test_check_negative_stock(product):
    with pytest.raises(Exception, match="Stock must be greater than or equal to 0"):
        product.check_negative_stock(-1)
