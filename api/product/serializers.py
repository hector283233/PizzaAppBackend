from rest_framework import serializers
from product.models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info
        fields = ["title", "mobile", "email", "address"]

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ["image", "banner_type"]

class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = ["delivery_price"]

class PSPOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSizePrice
        fields = ["id", "price", "size_tm", "size_ru", "purchase_count",
                  "purchase_point", "referer_point"]

class ProductListSerializer(serializers.ModelSerializer):
    size = PSPOutSerializer(source="product_psp", many=True)
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = ["id", "title_tm", "description_tm", "description_ru",
                  "image1", "image2", "image3", "image4", "image5", "image6",
                  "like_count", "is_new", "is_special", "is_cheap",
                  "category", "size"]