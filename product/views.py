from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from .models import *
from .serializer import *
from drf_spectacular.utils import extend_schema


class BrandViewSet(viewsets.ViewSet):
    queryset = Brand.objects.all()

    @extend_schema(responses=BrandSerializer)
    def list(self, request):
        serializer_data = BrandSerializer(self.queryset, many=True)
        return Response(serializer_data.data)


class CategoryViewSet(viewsets.ViewSet):
    queryset = Category.objects.all()

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer_data = CategorySerializer(self.queryset, many=True)
        return Response(serializer_data.data)


class ProductViewSet(viewsets.ViewSet):
    def get_queryset(self):
        return Product.objects.isactive()

    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        serializer_data = ProductSerializer(self.get_queryset(), many=True)
        return Response(serializer_data.data)

    # دکوریتور action به منظور ساخت یا اقدام غیر از اقدامات اصلی (مانند فیلترکردن و ...) می‌باشد
    # در این دکوریتور detail زمانی True‌است که صرفا یک داده توسط اکشن استخراج شود.
    @action(methods=['GET'], detail=False, url_path='category/(?P<category>.+)')
    def product_filter_with_category(self, request, category=None):
        # در متد فیلتر، category__name یعنی در جدول category ستون name مدنظر می‌باشد.
        serializer_data = ProductSerializer(self.get_queryset().filter(category__name=category), many=True)

        return Response(serializer_data.data)

    # به شیوه‌ی آدرس‌دهی که در url_path استفاده شده است regex گفته می‌شود.
    @action(methods=['GET'], detail=False, url_path='brand/(?P<brand>.+)')
    def product_filter_with_brand(self, request, brand=None):
        serializer_data = ProductSerializer(self.get_queryset().filter(brand__name=brand), many=True)

        return Response(serializer_data.data)

    # اکشن retrieve به منظور دریافت یک داده از دیتابیس به کمک pk می‌باشد.
    def retrieve(self, request, pk=None):
        # در روش یک خروجی یک لیست خواهد بود. اما با توجه به اینکه
        # این اکشن صرفا یک داده را برمیگرداند لیست عملا
        #  بی معنا می‌باشد. به همین دلیل از روشهای ۲ تا ۵ استفاده می‌شود
        #
        # روش یک
        # serializer_data = ProductSerializer(self.queryset.filter(pk=pk), many=True)
        #
        # روش دو: این روش با خطا مواجه خواهد شد چرا که خروجی filter فقط می‌تواند با many = True باشد.
        # serializer_data= ProductSerializer(self.queryset.filter(pk=pk))
        #
        # روش ۳: در این روش به کمک first فقط اولین داده ی فیلتر شده را میگیریم
        #  serializer_data = ProductSerializer(self.queryset.filter(pk=pk).first())
        #
        # روش ۴: با توجه به این که صرفا یک داده را به کمک آیدی میخواهیم دریافت کنیم
        # ، به جای فیلر کردن میتوان از get و آیدی استفاده کرد
        # serializer_data = ProductSerializer(self.queryset.get(pk=pk))
        #
        # روش ۵: روش قبلی در صورتی که آیدی‌ای وارد شود که در پایگاه داده وجود ندارد،
        # با ارور مواجه می‌شویم که نیاز است مدیریت خطا روی این ارور انجامم شود. علاوه بر
        # روش‌ گفته شده در جلسات قبل، می‌توان از تابع زیر استفاده نمود که در صورت عدم وجود آیدی خطای ۴۰۴ بدهد
        # بین تمامی روش‌های قبل، این روش بهترین روش خواهد بود.
        serializer_data = ProductSerializer(get_object_or_404(self.queryset, pk=pk))
        # به کمک get_object_or_404 تعریف می‌شود که در صورت عدم وجود آیدی ارور ۴۰۴ را برگرداند.
        return Response(serializer_data.data)
