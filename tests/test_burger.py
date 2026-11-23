import pytest
from praktikum.burger import Burger

class TestBurger:
    def test_new_burger_has_no_bun_and_no_ingredients(self, burger):
        assert burger.bun is None
        assert burger.ingredients == []

    def test_burgers_have_independent_ingredient_lists(self, burger, ingredient_factory):
        other = Burger()
        burger.add_ingredient(ingredient_factory())
        assert other.ingredients == []

    def test_set_buns_stores_selected_bun(self, burger, bun):
        burger.set_buns(bun)
        assert burger.bun is bun

    def test_set_buns_replaces_previous_bun(self, burger, bun):
        from unittest.mock import Mock
        from praktikum.bun import Bun
        other = Mock(spec=Bun)
        burger.set_buns(bun)
        burger.set_buns(other)
        assert burger.bun is other

    @pytest.mark.parametrize('count', [1, 2, 3])
    def test_add_ingredients_preserves_order(self, burger, ingredient_factory, count):
        ingredients = [ingredient_factory(name=f'Начинка {i}') for i in range(count)]
        for ingredient in ingredients:
            burger.add_ingredient(ingredient)
        assert burger.ingredients == ingredients

    def test_same_ingredient_can_be_added_twice(self, burger, ingredient_factory):
        ingredient = ingredient_factory()
        burger.add_ingredient(ingredient)
        burger.add_ingredient(ingredient)
        assert burger.ingredients == [ingredient, ingredient]

    @pytest.mark.parametrize('index,remaining', [(0, [1, 2]), (1, [0, 2]), (2, [0, 1])])
    def test_remove_ingredient_at_selected_position(self, burger, ingredient_factory, index, remaining):
        ingredients = [ingredient_factory(name=str(i)) for i in range(3)]
        burger.ingredients = ingredients.copy()
        burger.remove_ingredient(index)
        assert burger.ingredients == [ingredients[i] for i in remaining]

    def test_remove_last_ingredient_leaves_empty_list(self, burger, ingredient_factory):
        burger.ingredients = [ingredient_factory()]
        burger.remove_ingredient(0)
        assert burger.ingredients == []

    @pytest.mark.parametrize('source,target,order', [
        (0, 2, [1, 2, 0]), (2, 0, [2, 0, 1]),
        (0, 1, [1, 0, 2]), (1, 1, [0, 1, 2]),
    ])
    def test_move_ingredient_preserves_all_layers(self, burger, ingredient_factory, source, target, order):
        ingredients = [ingredient_factory(name=str(i)) for i in range(3)]
        burger.ingredients = ingredients.copy()
        burger.move_ingredient(source, target)
        assert burger.ingredients == [ingredients[i] for i in order]

    @pytest.mark.parametrize('bun_price,prices,expected', [
        (100, [], 200), (100, [50], 250), (100, [50, 25], 275),
        (0, [0], 0), (10.25, [0.5, 1.25], 22.25),
    ])
    def test_price_includes_two_bun_halves_and_all_ingredients(
        self, burger, bun, ingredient_factory, bun_price, prices, expected
    ):
        bun.get_price.return_value = bun_price
        burger.set_buns(bun)
        burger.ingredients = [ingredient_factory(price=price) for price in prices]
        assert burger.get_price() == pytest.approx(expected)

    def test_receipt_without_ingredients(self, burger, bun):
        burger.set_buns(bun)
        assert burger.get_receipt() == (
            '(==== Космическая булка ====)\n'
            '(==== Космическая булка ====)\n\nPrice: 200'
        )

    @pytest.mark.parametrize('kind,label', [('SAUCE', 'sauce'), ('FILLING', 'filling')])
    def test_receipt_contains_lowercase_type_name_and_total(
        self, burger, bun, ingredient_factory, kind, label
    ):
        burger.set_buns(bun)
        burger.add_ingredient(ingredient_factory('Марсианская начинка', 50, kind))
        assert burger.get_receipt() == (
            '(==== Космическая булка ====)\n'
            f'= {label} Марсианская начинка =\n'
            '(==== Космическая булка ====)\n\nPrice: 250'
        )

    def test_receipt_reflects_movement_and_removal(self, burger, bun, ingredient_factory):
        burger.set_buns(bun)
        burger.add_ingredient(ingredient_factory('Соус', 10, 'SAUCE'))
        burger.add_ingredient(ingredient_factory('Котлета', 20, 'FILLING'))
        burger.add_ingredient(ingredient_factory('Сыр', 30, 'FILLING'))
        burger.move_ingredient(2, 0)
        burger.remove_ingredient(1)
        assert burger.get_receipt() == (
            '(==== Космическая булка ====)\n'
            '= filling Сыр =\n= filling Котлета =\n'
            '(==== Космическая булка ====)\n\nPrice: 250'
        )
