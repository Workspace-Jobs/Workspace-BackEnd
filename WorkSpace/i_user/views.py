from rest_framework.pagination import PageNumberPagination
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


class NBTag(APIView):
    serializer_class = NBListSerializers
    pagination_class = PageNumberPagination
    pagination_class.page_size = 15

    def get(self, request):
        tag = request.query_params['tag']
        NB_O = NOTICE_BOARD.objects.filter(tag=tag).order_by('-id')
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(NB_O, request)
        serializer = NBListSerializers(result_page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NBList(APIView):
    serializer_class = NBListSerializers
    pagination_class = PageNumberPagination
    pagination_class.page_size = 15

    def get(self, request):
        NB_O = NOTICE_BOARD.objects.all().order_by('-id')
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(NB_O, request)
        serializer = NBListSerializers(result_page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NBDetail(APIView):
    serializer_class = NBDetailSerializers

    def get(self, request, pk):
        try:
            NB_O = NOTICE_BOARD.objects.get(pk=pk)
            serializer = NBDetailSerializers(NB_O, context={'request': request})
            serializer = serializer.data
            try:
                accessToken = request.META.get('HTTP_AUTHORIZATION')
                decoded_token = AccessToken(accessToken)
                decoded_payload = decoded_token.payload
                user = USER.objects.get(pk=decoded_payload["user_id"])
                good = GOOD.objects.get(user=user, nb=NB_O)
                serializer['good_bool'] = True
            except Exception:
                serializer['good_bool'] = False
            return Response(serializer, status=status.HTTP_200_OK)
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
    pagination_class = PageNumberPagination
    pagination_class.page_size = 15

    def get(self, request, pk):
        NB_O = NOTICE_BOARD.objects.get(pk=pk)
        C_list = COMMENT.objects.filter(nb=NB_O).order_by('-id')
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(C_list, request)
        serializer = COMMENTSerializers(result_page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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


class EMPLOYMENTList(APIView):
    serializer_class = EMPLOYMENTListSerializers
    pagination_class = PageNumberPagination
    pagination_class.page_size = 20

    def get(self, request):
        EM_O = EMPLOYMENT.objects.filter(date__gte=date.today()).order_by('-id')
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(EM_O, request)
        serializer = EMPLOYMENTListSerializers(result_page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EMPLOYMENTJobList(APIView):
    serializer_class = EMPLOYMENTListSerializers
    pagination_class = PageNumberPagination
    pagination_class.page_size = 20

    def get(self, request):
        job = request.query_params['job']
        if job in job_list:
            if job == "개발 전체":
                EM_O = EMPLOYMENT.objects.filter(date__gte=date.today()).order_by('-id')
            else:
                EM_O = EMPLOYMENT.objects.filter(Q(job=job) | Q(date__gte=date.today())).order_by('-id')
            paginator = self.pagination_class()
            result_page = paginator.paginate_queryset(EM_O, request)
            serializer = EMPLOYMENTListSerializers(result_page, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({
            "message": "아직 분류되지 않은 직종입니다."
        }, status=status.HTTP_400_BAD_REQUEST)


class EMPLOYMENTSearchList(APIView):
    serializer_class = EMPLOYMENTListSerializers
    pagination_class = PageNumberPagination
    pagination_class.page_size = 20

    def get(self, request):
        search = request.query_params['search']
        EM_O = EMPLOYMENT.objects.filter(
            Q(title__contains=search) | Q(job__contains=search) | Q(user__username__contains=search) | Q(
                date__gte=date.today())).order_by('-id')
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(EM_O, request)
        serializer = EMPLOYMENTListSerializers(result_page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EMPLOYMENTDetail(APIView):
    serializer_class = EMPLOYMENTDetailSerializers

    def get(self, request, pk):
        try:
            EM_O = EMPLOYMENT.objects.get(pk=pk)
            serializer = EMPLOYMENTDetailSerializers(EM_O)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response({
                "message": "채용 공고가 없습니다."
            })


class Mark(APIView):
    def get(self, request, pk):
        accessToken = request.META.get('HTTP_AUTHORIZATION')
        if verify_jwt(accessToken):
            decoded_token = AccessToken(accessToken)
            decoded_payload = decoded_token.payload
            user = USER.objects.get(pk=decoded_payload["user_id"])
            EM_O = EMPLOYMENT.objects.get(pk=pk)
            try:
                mark = MARK.objects.get(user=user, employment=EM_O)
                mark.delete()
                return Response({
                    "message": "북마트가 삭제 됐습니다."
                }, status=status.HTTP_204_NO_CONTENT)
            except Exception:
                mark = MARK()
                mark.user = user
                mark.employment = EM_O
                mark.save()
                return Response({
                    "message": "북마크에 추과 됐습니다."
                }, status=status.HTTP_204_NO_CONTENT)
        return Response({
            "message": "유효하지 않은 토큰입니다."
        }, status=status.HTTP_400_BAD_REQUEST)
