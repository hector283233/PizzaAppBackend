from rest_framework import serializers
from user.models import User, Mobile, Profile, RefId

class LoginInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
class LoginOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]
        
class RegisterMobileSerializer(serializers.Serializer):
    mobile = serializers.CharField()

class MobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mobile
        fields = "__all__"
        
class MobileVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Mobile
        fields = ["mobile", "sms_code"]
        
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"