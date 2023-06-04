from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC

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

    def get(self, request):
        accessToken = request.META.get('HTTP_AUTHORIZATION')
        if verify_jwt(accessToken):
            decoded_token = AccessToken(accessToken)
            decoded_payload = decoded_token.payload
            user = USER.objects.get(pk=decoded_payload["user_id"])
            R_list = RESUME.objects.filter(user=user)
            serializer = ResumeListSerializers(R_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({
            "message": "유효하지 않은 토큰입니다."
        }, status=status.HTTP_400_BAD_REQUEST)


class ResumeDetail(APIView):
    def get(self, request, pk):
        accessToken = request.META.get('HTTP_AUTHORIZATION')
        if verify_jwt(accessToken):
            decoded_token = AccessToken(accessToken)
            decoded_payload = decoded_token.payload
            user = USER.objects.get(pk=decoded_payload["user_id"])
            resume = RESUME.objects.get(pk=pk)
            if resume.user == user:
                serializer = ResumeSerializers(resume)
                return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
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
            try:
                accessToken = request.META.get('HTTP_AUTHORIZATION')
                decoded_token = AccessToken(accessToken)
                decoded_payload = decoded_token.payload
                user = USER.objects.get(pk=decoded_payload["user_id"])
                bools = SUPPORT.objects.get(employment=EM_O, user=user)
                EM_O.support_bool = True
            except Exception:
                EM_O.support_bool = False
            finally:
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


class Support(APIView):
    serializer_class = SUPPORTSerializers

    def post(self, request, pk):
        accessToken = request.META.get('HTTP_AUTHORIZATION')
        if verify_jwt(accessToken):
            decoded_token = AccessToken(accessToken)
            decoded_payload = decoded_token.payload
            user = USER.objects.get(pk=decoded_payload["user_id"])
            EM_O = EMPLOYMENT.objects.get(pk=pk)
            serializer = SUPPORTSerializers(data=request.data)
            if serializer.is_valid():
                RE_pk = serializer.validated_data.get('resume')
                RE = RESUME.objects.get(pk=int(RE_pk))
                serializer.save(user=user, employment=EM_O, resume=RE, state="서류 접수")
                return Response({
                    "message": "서류 접수 됐습니다."
                })
            return Response({
                "message": "잘못된 요청입니다."
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "message": "유효하지 않은 토큰입니다."
        }, status=status.HTTP_400_BAD_REQUEST)


class MyPageUser(APIView):
    serializer_class = USERMyPageSerializers

    def get(self, request):
        accessToken = request.META.get('HTTP_AUTHORIZATION')
        if verify_jwt(accessToken):
            decoded_token = AccessToken(accessToken)
            decoded_payload = decoded_token.payload
            user = USER.objects.get(pk=decoded_payload["user_id"])
            serializer = USERMyPageSerializers(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({
            "message": "유효하지 않은 토큰입니다."
        }, status=status.HTTP_400_BAD_REQUEST)


class MyPageMark(APIView):
    serializer_class = MyPageMarkSerializers

    def get(self, request):
        accessToken = request.META.get('HTTP_AUTHORIZATION')
        if verify_jwt(accessToken):
            decoded_token = AccessToken(accessToken)
            decoded_payload = decoded_token.payload
            try:
                user = USER.objects.get(pk=decoded_payload["user_id"])
            except Exception:
                return Response({
                    "message": "사용자가 없습니다."
                }, status=status.HTTP_400_BAD_REQUEST)
            mark = MARK.objects.filter(user=user).order_by("-id")
            serializer = MyPageMarkSerializers(mark, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({
            "message": "유효하지 않은 토큰입니다."
        }, status=status.HTTP_400_BAD_REQUEST)


class MyPageGood(APIView):
    serializer_class = MyPageGoodSerializers

    def get(self, request):
        accessToken = request.META.get('HTTP_AUTHORIZATION')
        if verify_jwt(accessToken):
            decoded_token = AccessToken(accessToken)
            decoded_payload = decoded_token.payload
            try:
                user = USER.objects.get(pk=decoded_payload["user_id"])
            except Exception:
                return Response({
                    "message": "사용자가 없습니다."
                }, status=status.HTTP_400_BAD_REQUEST)
            good = GOOD.objects.filter(user=user).order_by("-id")
            serializer = MyPageGoodSerializers(good, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({
            "message": "유효하지 않은 토큰입니다."
        }, status=status.HTTP_400_BAD_REQUEST)


class MyPageMyNB(APIView):
    serializer_class = NBListSerializers

    def get(self, request):
        accessToken = request.META.get('HTTP_AUTHORIZATION')
        if verify_jwt(accessToken):
            decoded_token = AccessToken(accessToken)
            decoded_payload = decoded_token.payload
            try:
                user = USER.objects.get(pk=decoded_payload["user_id"])
            except Exception:
                return Response({
                    "message": "사용자가 없습니다."
                }, status=status.HTTP_400_BAD_REQUEST)
            good = NOTICE_BOARD.objects.filter(user=user).order_by("-id")
            serializer = NBListSerializers(good, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({
            "message": "유효하지 않은 토큰입니다."
        }, status=status.HTTP_400_BAD_REQUEST)


class UserProfile(APIView):
    serializer_class = UserProfileSerializers

    def post(self, request):
        accessToken = request.META.get('HTTP_AUTHORIZATION')
        if verify_jwt(accessToken):
            decoded_token = AccessToken(accessToken)
            decoded_payload = decoded_token.payload
            user = USER.objects.get(pk=decoded_payload["user_id"])
            serializer = UserProfileSerializers(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "이미지가 변경됐습니다."
                }, status=status.HTTP_200_OK)
            return Response({
                "message": "잘못등록 됐습니다."
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "message": "유효하지 않은 토큰입니다."
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        accessToken = request.META.get('HTTP_AUTHORIZATION')
        if verify_jwt(accessToken):
            decoded_token = AccessToken(accessToken)
            decoded_payload = decoded_token.payload
            user = USER.objects.get(pk=decoded_payload["user_id"])
            user.profile = 'profile/default.png'
            user.save()
            return Response({
                "message": "프로필이 기본 이미지로 변경됩니다."
            }, status=status.HTTP_204_NO_CONTENT)
        return Response({
            "message": "유효하지 않은 토큰입니다."
        }, status=status.HTTP_400_BAD_REQUEST)


class UserName(APIView):
    serializer_class = UserNameSerializers

    def post(self, request):
        accessToken = request.META.get('HTTP_AUTHORIZATION')
        if verify_jwt(accessToken):
            decoded_token = AccessToken(accessToken)
            decoded_payload = decoded_token.payload
            user = USER.objects.get(pk=decoded_payload["user_id"])
            serializer = UserNameSerializers(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "이름이 등록됐습니다."
                }, status=status.HTTP_200_OK)
            return Response({
                "message": "잘못된 요청입니다."
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "message": "유효하지 않은 토큰입니다."
        }, status=status.HTTP_400_BAD_REQUEST)


class StateNum(APIView):
    def get(self, request):
        accessToken = request.META.get('HTTP_AUTHORIZATION')
        if verify_jwt(accessToken):
            decoded_token = AccessToken(accessToken)
            decoded_payload = decoded_token.payload
            user = USER.objects.get(pk=decoded_payload["user_id"])
            data_1 = SUPPORT.objects.filter(user=user, state="지원 완료")
            data_2 = SUPPORT.objects.filter(user=user, state="서류 통과")
            data_3 = SUPPORT.objects.filter(user=user, state="최종 합격")
            data_4 = SUPPORT.objects.filter(user=user, state="불합격")
            return Response({
                "지원 완료": len(data_1),
                "서류 통과": len(data_2),
                "최종 합격": len(data_3),
                "불합격": len(data_4)
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "유효하지 않은 토큰입니다."
        }, status=status.HTTP_400_BAD_REQUEST)


class StateList(APIView):
    def get(self, request):
        accessToken = request.META.get('HTTP_AUTHORIZATION')
        if verify_jwt(accessToken):
            decoded_token = AccessToken(accessToken)
            decoded_payload = decoded_token.payload
            user = USER.objects.get(pk=decoded_payload["user_id"])
            state = request.query_params['state']
            data = SUPPORT.objects.filter(user=user, state=state).order_by("-id")
            serializer = SUPPORTListSerializers(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({
            "message": "유효하지 않은 토큰입니다."
        }, status=status.HTTP_400_BAD_REQUEST)


class SupportDetail(APIView):
    def get(self, request, pk):
        accessToken = request.META.get('HTTP_AUTHORIZATION')
        if verify_jwt(accessToken):
            decoded_token = AccessToken(accessToken)
            decoded_payload = decoded_token.payload
            user = USER.objects.get(pk=decoded_payload["user_id"])
            support = SUPPORT.objects.get(pk=pk)
            if user == support.user:
                serializer = SUPPORTDetailSerializers(support)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({
                "message": "유저가 다릅니다."
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
            support = SUPPORT.objects.get(pk=pk)
            if user == support.user:
                support.delete()
                return Response({
                    "message": "지원이 취소됐습니다."
                }, status=status.HTTP_204_NO_CONTENT)
            return Response({
                "message": "유저가 다릅니다."
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "message": "유효하지 않은 토큰입니다."
        }, status=status.HTTP_400_BAD_REQUEST)


class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        confirmation.confirm(self.request)
        return HttpResponseRedirect('/')

    def get_object(self, queryset=None):
        key = self.kwargs['key']
        email_confirmation = EmailConfirmationHMAC.from_key(key)
        if not email_confirmation:
            if queryset is None:
                queryset = self.get_queryset()
            try:
                email_confirmation = queryset.get(key=key.lower())
            except EmailConfirmation.DoesNotExist:
                return HttpResponseRedirect('/')
        return email_confirmation

    def get_queryset(self):
        qs = EmailConfirmation.objects.all_valid()
        qs = qs.select_related("email_address__user")
        return qs


def index(request):
    return render(request, 'index.html')


class UserMain(APIView):
    def get(self, request):
        accessToken = request.META.get('HTTP_AUTHORIZATION')
        if verify_jwt(accessToken):
            decoded_token = AccessToken(accessToken)
            decoded_payload = decoded_token.payload
            user = USER.objects.get(pk=decoded_payload["user_id"])
            serializer = UserMainSerializers(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({
            "message": "유효하지 않은 토큰입니다."
        }, status=status.HTTP_400_BAD_REQUEST)
