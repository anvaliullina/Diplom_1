from unittest.mock import Mock
import pytest
from praktikum.bun import Bun
from praktikum.burger import Burger
from praktikum.ingredient import Ingredient

@pytest.fixture
def burger():
    return Burger()

@pytest.fixture
def bun():
    mock = Mock(spec=Bun)
    mock.get_name.return_value = 'Космическая булка'
    mock.get_price.return_value = 100
    return mock

@pytest.fixture
def ingredient_factory():
    def make(name='Начинка', price=50, kind='FILLING'):
        mock = Mock(spec=Ingredient)
        mock.get_name.return_value = name
        mock.get_price.return_value = price
        mock.get_type.return_value = kind
        return mock
    return make
