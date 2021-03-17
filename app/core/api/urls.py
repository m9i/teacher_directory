from rest_framework import serializers, viewsets, routers
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('teacher-list/', TeacherAPIView.as_view()),
]