from django.urls import path, include
from rest_framework import routers

from .views import *

urlpatterns = [
    path('user/', include('dj_rest_auth.urls')),
    path('user/registration/', include('dj_rest_auth.registration.urls')),

    path('user/resume/', Resume.as_view()),
    path('user/resume/<int:pk>', ResumeDetail.as_view()),

    path('NB/', NB.as_view()),
    path('NB/<int:pk>', NBDetail.as_view()),
    path('NB/list/', NBList.as_view()),
    path('NB/list/tag/', NBTag.as_view()),
    path('NB/good/<int:pk>', Good.as_view()),
    path('NB/comment/<int:pk>', Comment.as_view()),


]
