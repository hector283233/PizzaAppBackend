from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.hashers import make_password
import random
from GlobalVariables import *

from user.models import User, Profile, Mobile
from .serializers import *

class LoginUser(APIView):
    @swagger_auto_schema(
        operation_summary="Login User",
        request_body = LoginInSerializer
    )
    def post(self, request):
        data = request.data
        if 'password' in data:
            if data['password'] == None or data['password'] == "":
                return Response({
                    "response": "error",
                    "message": MSG_NO_PASSWORD
                }, status=status.HTTP_400_BAD_REQUEST)
            if 'username' not in data:
                return Response({
                    "response":"error",
                    "message": MSG_NO_USER_INFO
                }, status=status.HTTP_400_BAD_REQUEST)
            
            password = data['password']
            username = data['username']
            user = authenticate(username=username, password=password)
            if user is None:
                return Response({
                    "response": "error",
                    "message": MSG_USERNAME_OR_PASSWORD_ERROR
                }, status=status.HTTP_400_BAD_REQUEST)
        serializer = LoginOutSerializer(user)
        refresh = RefreshToken.for_user(user)
        return Response({"response": "success",
                         "refresh": str(refresh),
                         "access": str(refresh.access_token),
                         "user": serializer.data})

# ======= REGISTER MOBILE ======== #
@swagger_auto_schema(
    methods=['POST'],
    request_body=RegisterMobileSerializer
)
@api_view(['POST'])
def registerMobile(request):
    try:
        data = request.data
        generated_code = random.randint(1000, 9999)
        data['sms_code'] = generated_code
        if Mobile.objects.filter(mobile=data["mobile"]).exists():
            tMobile = Mobile.objects.get(mobile=data['mobile'])
            tMobile.is_sms_sent = False
            tMobile.is_verified = False
            tMobile.sms_code = generated_code
            tMobile.save()
            user = User.objects.filter(username=data['mobile']).first()
            if user:
                user.password = make_password(str(data['sms_code']))
                user.save()
                return Response({"response":"success", 
                                "message": SUCCESS_MESSAGE_MOBILE})
            else:
                return Response({
                    "response": "error",
                    "message": "Mobile registered but user did not register."
                }, status=status.HTTP_400_BAD_REQUEST)
        serializer = MobileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.create(
                username = data['mobile'],
                password = make_password(serializer.data['sms_code'])
            )
            return Response({"response":"success", "message": SUCCESS_MESSAGE_MOBILE},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({"response":"error", "message": MSG_PARAMETERS_INSUFFICIENT},
                            status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"response":"error"}, status=status.HTTP_400_BAD_REQUEST)

# ======= SMS LIST ======= #
@swagger_auto_schema(
    methods=['GET'],
    responses={200: MobileVerifySerializer}
)
@api_view(['GET'])
def smsList(request):
    tMobiles = Mobile.objects.filter(is_sms_sent=False)
    for mobile in tMobiles:
        mobile.is_sms_sent = True
        mobile.save()
    serializer = MobileVerifySerializer(tMobiles, many=True)
    return Response({"response": "success", "data": serializer.data},
                    status=status.HTTP_200_OK)

# ====== USER DETAIL ======= #
@swagger_auto_schema(
    operation_summary='User Detail',
    methods=['GET'],
    responses={200: UserDetailSerializer}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userDetail(request):
    user = request.user
    serializer = UserDetailSerializer(user)
    return Response({"response":"success","data":serializer.data},
                    status=status.HTTP_200_OK)