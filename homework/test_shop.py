"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    @pytest.mark.parametrize("quantity", [1, 1000, 1001])
    def test_product_check_quantity(self, product, quantity):
        # TODO напишите проверки на метод check_quantity
        if quantity <= product.quantity:
            assert product.check_quantity(quantity) is True
        else:
            assert product.check_quantity(quantity) is False

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        product.buy(1)
        assert product.quantity == 999
        product.buy(999)
        assert product.quantity == 0

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError, match="Продуктов не хватает"):
            product.buy(1001)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product_to_cart(self, cart, product):
        """
        Добавляем товары в корзину
        """
        cart.add_product(product, buy_count=1)
        assert cart.products[product] == 1

        cart.add_product(product, buy_count=2)
        assert cart.products[product] == 3

    def test_cart_remove_all_product(self, cart, product):
        """
        Удаляем все позиции товара из корзины
        """
        cart.add_product(product, buy_count=2)
        cart.remove_product(product)
        assert product not in cart.products

    def test_cart_remove_more_product(self, cart, product):
        """
        Удаляем больше товаров, чем есть в корзине
        """
        cart.add_product(product)
        cart.remove_product(product, remove_count=2)
        assert product not in cart.products

    def test_cart_remove_one_product(self, cart, product):
        """
        Удаляем один товар из корзины
        """
        cart.add_product(product, buy_count=2)
        cart.remove_product(product, remove_count=1)
        assert cart.products[product] == 1

    def test_clear_cart_with_products(self, cart, product):
        """
        Очищаем корзину, в которой есть товары
        """
        cart.add_product(product, buy_count=1)
        assert cart.products[product] == 1
        cart.clear()
        assert product not in cart.products

    def test_get_total_price_in_cart(self, cart, product):
        """
        Считаем итоговую стоимость товаров в корзине
        """
        cart.add_product(product, buy_count=3)
        cart.get_total_price()
        assert cart.get_total_price() == 300

    def test_cart_buy_products(self, product, cart):
        """
        Покупаем товары
        """
        cart.add_product(product, buy_count=5)
        assert cart.products[product] == 5
        cart.buy()
        assert product.quantity == 995
        assert cart.products == {}

    def test_cart_buy_more_than_available(self, cart, product):
        cart.add_product(product, buy_count=1001)
        with pytest.raises(ValueError, match="Товаров не хватает на складе"):
            cart.buy()
