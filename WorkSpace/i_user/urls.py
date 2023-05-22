from django.urls import path, include
from rest_framework import routers

from .views import *

urlpatterns = [
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),

    path('user/resume/', Resume.as_view()),
    path('user/resume/<int:pk>', ResumeDetail.as_view()),

    path('NB/', NB.as_view()),
    path('NB/<int:pk>', NBDetail.as_view()),
]
