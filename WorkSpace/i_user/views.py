from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.parsers import JSONParser
from django.db.models import Q
from datetime import date, timedelta
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

from .models import *
from .serializers import *
from .filter import *


def verify_jwt(token):
    try:
        JWTAuthentication().get_validated_token(token)
        return True
    except InvalidToken:
        return False


class Resume(APIView):
    serializer_class = ResumeSerializers

    def post(self, request):
        accessToken = request.META.get('HTTP_AUTHORIZATION')
        if verify_jwt(accessToken):
            decoded_token = AccessToken(accessToken)
            decoded_payload = decoded_token.payload
            user = USER.objects.get(pk=decoded_payload["user_id"])
            serializer = ResumeSerializers(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user)
                return Response({
                    "message": "이력서가 등록됐습니다."
                }, status=status.HTTP_200_OK)
            return Response({
                "message": "잘못된 요청입니다."
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "message": "유효하지 않은 토큰입니다."
        }, status=status.HTTP_400_BAD_REQUEST)


class ResumeDetail(APIView):
    def delete(self, request, pk):
        accessToken = request.META.get('HTTP_AUTHORIZATION')
        if verify_jwt(accessToken):
            decoded_token = AccessToken(accessToken)
            decoded_payload = decoded_token.payload
            user = USER.objects.get(pk=decoded_payload["user_id"])
            resume = RESUME.objects.get(pk=pk)
            if resume.user == user:
                resume.delete()
                return Response({
                    "message": "삭제되었습니다."
                }, status=status.HTTP_204_NO_CONTENT)
            return Response({
                "message": "사용자가 다릅니다."
            }, status=status.HTTP_204_NO_CONTENT)
        return Response({
            "message": "유효하지 않은 토큰입니다."
        }, status=status.HTTP_400_BAD_REQUEST)


class NB(APIView):
    serializer_class = NBDetailSerializers

    def post(self, request):
        accessToken = request.META.get('HTTP_AUTHORIZATION')
        if verify_jwt(accessToken):
            decoded_token = AccessToken(accessToken)
            decoded_payload = decoded_token.payload
            user = USER.objects.get(pk=decoded_payload["user_id"])
            serializer = NBDetailSerializers(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user)
                return Response({
                    "message": "게시물이 등록됐습니다."
                }, status=status.HTTP_200_OK)
            return Response({
                "message": "잘못된 요청입니다."
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "message": "유효하지 않은 토큰입니다."
        }, status=status.HTTP_400_BAD_REQUEST)


class NBDetail(APIView):
    serializer_class = NBDetailSerializers

    def get(self, request, pk):
        try:
            NB_O = NOTICE_BOARD.objects.get(pk=pk)
            serializer = NBDetailSerializers(NB_O)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response({
                "message": "pk가 없습니다."
            },status=status.HTTP_400_BAD_REQUEST)
        
