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

def test_decrease_stock_below_zero(product):
    with pytest.raises(Exception) as excinfo:
        product.decrease_stock(15)
    assert str(excinfo.value) == "Stock must be greater than or equal to 0"

def test_increase_stock_with_non_positive_value(product):
    with pytest.raises(Exception) as excinfo:
        product.increase_stock(0)
    assert str(excinfo.value) == "Number must be positive"

def test_increase_stock_with_negative_value(product):
    with pytest.raises(Exception) as excinfo:
        product.increase_stock(-5)
    assert str(excinfo.value) == "Number must be positive"

def test_decrease_stock_with_non_positive_value(product):
    with pytest.raises(Exception) as excinfo:
        product.decrease_stock(0)
    assert str(excinfo.value) == "Number must be positive"

def test_decrease_stock_with_negative_value(product):
    with pytest.raises(Exception) as excinfo:
        product.decrease_stock(-5)
    assert str(excinfo.value) == "Number must be positive"
