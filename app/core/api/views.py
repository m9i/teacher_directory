from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from .serializers import *
from core.models import *


class TeacherAPIView(generics.ListAPIView):
    search_fields = [
                    'last_name',
                    'subjects',
                     ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {'last_name': [ 'startswith',],
                         'subjects': [ 'startswith',],
                         }
    queryset = Teacher.objects.all().order_by('-id')
    serializer_class = TeacherSerializer