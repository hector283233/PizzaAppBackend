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