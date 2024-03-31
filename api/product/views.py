from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from .serializers import *
from GlobalVariables import *

from product.models import (Category, Info, Group)
from user.models import User

class GeneralInfo(APIView):
    @swagger_auto_schema(
        operation_summary="App Info"
    )
    def get(self, request):
        categories = Category.objects.all()
        info = Info.objects.first()
        serializer_category = CategorySerializer(categories, many=True)
        serializer_info = InfoSerializer(info)
        banners = Banner.objects.filter(banner_type="MAIN")[:3]
        serializer_banner = BannerSerializer(banners, many=True)
        setting = Settings.objects.first()
        serializer_settings = SettingsSerializer(setting)
        return Response({"response":"success",
                         "data": {
                             "categories": serializer_category.data,
                             "info": serializer_info.data,
                             "banners": serializer_banner.data,
                             "settings": serializer_settings.data,
                         }})

class ProductFilter(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductListSerializer(products, many=True)
        return Response({"response":"success", "data": serializer.data})

class ComboFilter(APIView):
    def get(self, request):
        groups = Group.objects.all()
        serializer = GroupListSerializer(groups, many=True)
        return Response({'response': 'success', 'data': serializer.data})