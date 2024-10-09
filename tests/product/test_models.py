import pytest
from django.core.exceptions import ValidationError
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


class TestProductLine:
    def test_str_method(self, product_line_factory):

        new_productline = product_line_factory(sku='xl')

        assert new_productline.__str__() == 'xl'

    def test_duplicate_order(self,product_line_factory,product_factory):
        prd_factory = product_factory()
        product_line_factory(order=1, product=prd_factory)
        with pytest.raises(ValidationError):
            product_line_factory(order=1, product=prd_factory).clean_fields(None)

