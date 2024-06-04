import pytest
import main
from main import LinkedList, Node

def test_init_empty():
    ll = LinkedList()
    assert ll.head is None
    assert ll.tail is None

def test_init_with_items():
    items = [1, 2, 3]
    ll = LinkedList(items)
    assert ll.items() == items
    