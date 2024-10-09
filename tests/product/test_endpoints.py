import pytest
import json
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


class TestCategoryEndpoint:

    def test_category_endpoint(self, category_factory):

        category_factory.create_batch(4)
        response = APIClient().get("/api/category/")

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 4


class TestProductEndpoint:
    def test_get_all_product(self, product_factory):

        product_factory.create_batch(4)

        response = APIClient().get("/api/product/")

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 4

    def test_get_product_with_id(self, product_factory):

        obj=product_factory(name='test')

        response = APIClient().get(f"/api/product/{obj.id}")

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 6

    def test_get_product_with_category(self, product_factory, category_factory):
        fake_category = category_factory()
        product_factory(category=fake_category)

        response = APIClient().get(f"/api/product/category/{fake_category.name}/")

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    def test_get_product_with_brand(self, product_factory, brand_factory):
        fake_brand = brand_factory()
        product_factory(brand=fake_brand)
        product_factory(brand=fake_brand)
        product_factory()
        response = APIClient().get(f"/api/product/brand/{fake_brand.name}/")
        print(json.loads(response.content))

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 2


class TestBrandEndpoint:

    def test_brand_endpoint(self, brand_factory):

        brand_factory.create_batch(4)
        response = APIClient().get("/api/brand/")

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 4
