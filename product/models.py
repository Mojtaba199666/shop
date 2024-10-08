from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from .fields import OrderField
from django.core.exceptions import ValidationError


class ActiveQuerySet(models.QuerySet):

    def isactive(self):
        return self.filter(is_active=True)


class Category(MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to='Product_pic/', default='/Product_pic/default.jpg')
    is_digital = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    category = TreeForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    objects = ActiveQuerySet.as_manager()

    def __str__(self):
        return self.name


class ProductLine(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=100)
    stock_qty = models.IntegerField()
    is_active = models.BooleanField(default=True)

    product = models.ForeignKey(Product, on_delete=models.CASCADE,default=1, related_name='product_line')
    order = OrderField(unique_for_field='product', blank=True)
    objects = ActiveQuerySet.as_manager()

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude)

        filter_object = ProductLine.objects.filter(product=self.product)

        for item in filter_object:
            if item.order == self.order and item.id != self.id:
                raise ValidationError("order can't be duplicate")

    def __str__(self):
        return self.sku
