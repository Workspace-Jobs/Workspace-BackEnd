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
            }, status=status.HTTP_400_BAD_REQUEST)
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
            }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        accessToken = request.META.get('HTTP_AUTHORIZATION')
        if verify_jwt(accessToken):
            decoded_token = AccessToken(accessToken)
            decoded_payload = decoded_token.payload
            user = USER.objects.get(pk=decoded_payload["user_id"])
            NB_O = NOTICE_BOARD.objects.get(pk=pk)
            if user == NB_O.user:
                serializer = NBDetailSerializers(NB_O, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        "message": "게시물이 수정됐습니다."
                    }, status=status.HTTP_200_OK)
                return Response({
                    "message": "잘못된 요청입니다."
                }, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                "message": "사용자가 다릅니다."
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "message": "유효하지 않은 토큰입니다."
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        accessToken = request.META.get('HTTP_AUTHORIZATION')
        if verify_jwt(accessToken):
            decoded_token = AccessToken(accessToken)
            decoded_payload = decoded_token.payload
            user = USER.objects.get(pk=decoded_payload["user_id"])
            NB_O = NOTICE_BOARD.objects.get(pk=pk)
            if NB_O.user == user:
                NB_O.delete()
                return Response({
                    "message": "삭제되었습니다."
                }, status=status.HTTP_204_NO_CONTENT)
            return Response({
                "message": "사용자가 다릅니다."
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "message": "유효하지 않은 토큰입니다."
        }, status=status.HTTP_400_BAD_REQUEST)


class Good(APIView):
    def get(self, request, pk):
        accessToken = request.META.get('HTTP_AUTHORIZATION')
        if verify_jwt(accessToken):
            decoded_token = AccessToken(accessToken)
            decoded_payload = decoded_token.payload
            user = USER.objects.get(pk=decoded_payload["user_id"])
            NB_O = NOTICE_BOARD.objects.get(pk=pk)
            try:
                good = GOOD.objects.get(user=user, nb=NB_O)
                good.delete()
                return Response({
                    "message": "좋아요가 삭제 됐습니다."
                }, status=status.HTTP_204_NO_CONTENT)
            except Exception:
                good = GOOD()
                good.user = user
                good.nb = NB_O
                good.save()
                return Response({
                    "message": "좋아요가 추과 됐습니다."
                }, status=status.HTTP_204_NO_CONTENT)
        return Response({
            "message": "유효하지 않은 토큰입니다."
        }, status=status.HTTP_400_BAD_REQUEST)


class Comment(APIView):
    serializer_class = COMMENTSerializers

    def get(self, request, pk):
        NB_O = NOTICE_BOARD.objects.get(pk=pk)
        C_list = COMMENT.objects.filter(nb=NB_O).order_by('-id')
        serializer = COMMENTSerializers(C_list, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self, request, pk):
        accessToken = request.META.get('HTTP_AUTHORIZATION')
        if verify_jwt(accessToken):
            decoded_token = AccessToken(accessToken)
            decoded_payload = decoded_token.payload
            user = USER.objects.get(pk=decoded_payload["user_id"])
            NB_O = NOTICE_BOARD.objects.get(pk=pk)
            serializer = COMMENTSerializers(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user, nb=NB_O)
                return Response({
                    "message": "댓글이 추과 됐습니다."
                }, status=status.HTTP_204_NO_CONTENT)
            return Response({
                "message": "잘못된 요청입니다."
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "message": "유효하지 않은 토큰입니다."
        }, status=status.HTTP_400_BAD_REQUEST)
