from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from .serializers import *
from core.models import *


class TeacherAPIView(generics.ListAPIView):
    search_fields = [
                    'last_name',
                    'subjects__name',
                     ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {'last_name': [ 'startswith',],
                         'subjects__name': [ 'startswith',],
                         }
    queryset = Teacher.objects.all().order_by('-id')
    serializer_class = TeacherSerializer
    
class SubjectAPIView(generics.ListAPIView):
    search_fields = [
                    'name',
                     ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {'name': [ 'startswith',],
                         }
    queryset = Subject.objects.all().order_by('-id')
    serializer_class = SubjectSerializer