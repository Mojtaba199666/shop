import factory

from product.models import Category, Brand, Product, ProductLine


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.sequence(lambda x: f"category_test_{x}")


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.sequence(lambda x: f"brand_test_{x}")


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.sequence(lambda x: f"product_test_{x}")
    description = factory.Faker('paragraph')
    category = factory.SubFactory(CategoryFactory)
    brand = factory.SubFactory(BrandFactory)


class ProductLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductLine

    price = 100
    sku = factory.sequence(lambda x: f"sku_{x}")
    stock_qty = 1
    is_active = True
    product = factory.SubFactory(ProductFactory)

