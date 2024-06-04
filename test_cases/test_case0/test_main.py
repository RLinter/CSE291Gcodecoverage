from test_cases.test_case0.main import Product
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
