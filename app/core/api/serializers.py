from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination


from core.models import *


class TeacherSerializer(serializers.ModelSerializer):
    page_size = 10
    
    class Meta:
        model = Teacher
        fields = '__all__'
        
        
class TeacherBulkUploadSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TeacherBulkUpload
        fields = '__all__'
        
class SubjectSerializer(serializers.ModelSerializer):
    teachers = TeacherSerializer(many=True, read_only=True)
    
    class Meta:
        model = Subject
        fields = '__all__'