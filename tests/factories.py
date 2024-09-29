import factory

from product.models import Category, Brand, Product


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

