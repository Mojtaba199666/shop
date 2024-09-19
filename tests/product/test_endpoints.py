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
    def test_product_endpoint(self, product_factory):

        product_factory.create_batch(4)

        response = APIClient().get("/api/product/")

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 4


class TestBrandEndppoint:

    def test_brand_endpoint(self, brand_factory):

        brand_factory.create_batch(4)
        response = APIClient().get("/api/brand/")

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 4
