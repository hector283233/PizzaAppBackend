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
        fields = "__all__"

class PSPOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSizePrice
        fields = ["id", "price", "size_tm", "size_ru", "purchase_count",
                  "purchase_point", "referer_point"]
        
class PSPMiniOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSizePrice
        fields = ["id", 'price', 'size_tm', 'size_ru']

class RPOutSerializer(serializers.ModelSerializer):
    # size = PSPOutSerializer(source="product_psp", many=True)
    size = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'title_tm', 'title_ru', 'image1', 'size']
    
    def get_size(self, obj):
        sizes = ProductSizePrice.objects.filter(product=obj).first()
        serializer = PSPMiniOutSerializer(sizes)
        return serializer.data

class RelatedProductListSerializer(serializers.ModelSerializer):
    product = RPOutSerializer(source="related_product")
    class Meta:
        model = RelatedProducts
        fields = ['product']
    


class ProductListSerializer(serializers.ModelSerializer):
    size = PSPOutSerializer(source="product_psp", many=True)
    category = CategorySerializer()
    related_products = RelatedProductListSerializer(source="related_product", many=True)

    class Meta:
        model = Product
        fields = ["id", "title_tm", "title_ru", "description_tm", "description_ru",
                  "image1", "image2", "image3", "image4", "image5", "image6",
                  "like_count", "is_new", "is_special", "is_cheap",
                  "related_products", "category", "size"]
        
class GroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'image', 'title_tm', 'title_ru', 'description_tm',
                  'description_ru', 'total_price', 'purchase_point', 'product']
        # fields = "__all__"