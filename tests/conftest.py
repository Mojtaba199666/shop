from pytest_factoryboy import register

from factories import CategoryFactory, BrandFactory, ProductFactory, ProductLineFactory

register(CategoryFactory)
register(BrandFactory)
register(ProductFactory)
register(ProductLineFactory)
