import pytest

pytestmark = pytest.mark.django_db


class TestCategory:
    def test_str_category(self, category_factory):

        new_category = category_factory()

        assert new_category.__str__() == new_category.name


class TestBrand:
    def test_str_brand(self, brand_factory):

        new_brand = brand_factory()

        assert str(new_brand) == new_brand.name


class TestProduct:
    def test_str_product(self, product_factory):

        new_product = product_factory()

        assert str(new_product) == new_product.name
