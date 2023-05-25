from django.urls import path, include
from django.urls import re_path
from dj_rest_auth.registration.views import VerifyEmailView

from .views import *

urlpatterns = [
    path('', index),

    path('user/', include('dj_rest_auth.urls')),
    path('user/registration/', include('dj_rest_auth.registration.urls')),
    re_path(r'^account-confirm-email/$', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(), name='account_confirm_email'),
    path('user/name/', UserName.as_view()),
    path('user/main/', UserMain.as_view()),

    path('user/resume/', Resume.as_view()),
    path('user/resume/<int:pk>', ResumeDetail.as_view()),

    path('NB/', NB.as_view()),
    path('NB/<int:pk>', NBDetail.as_view()),
    path('NB/list/', NBList.as_view()),
    path('NB/list/tag/', NBTag.as_view()),
    path('NB/good/<int:pk>', Good.as_view()),
    path('NB/comment/<int:pk>', Comment.as_view()),

    path('EM/', EMPLOYMENTList.as_view()),
    path('EM/job/', EMPLOYMENTJobList.as_view()),
    path('EM/search/', EMPLOYMENTSearchList.as_view()),
    path('EM/<int:pk>', EMPLOYMENTDetail.as_view()),
    path('EM/mark/<int:pk>', Mark.as_view()),
    path('EM/su/<int:pk>', Support.as_view()),

    path('NP/user/', MyPageUser.as_view()),
    path('NP/mark/', MyPageMark.as_view()),
    path('NP/good/', MyPageGood.as_view()),
    path('NP/NB/', MyPageMyNB.as_view()),
    path('NP/profile/', UserProfile.as_view()),
    path('NP/state/', StateNum.as_view()),
    path('NP/state/list/', StateList.as_view()),
    path('NP/support/<int:pk>', SupportDetail.as_view()),
]
