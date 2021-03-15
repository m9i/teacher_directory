from django.urls import path

from .views import *


urlpatterns = [
  path('', IndexView.as_view(), name='home'),
  path('list', teacher_list, name='teacher-list'),
  path('<int:pk>/', TeacherDetailView.as_view(), name='teacher-detail'),
  path('create/', TeacherCreateView.as_view(), name='teacher-create'),
  path('<int:pk>/update/', TeacherUpdateView.as_view(), name='teacher-update'),
  path('delete/<int:pk>/', TeacherDeleteView.as_view(), name='teacher-delete'),

  path('upload/', TeacherBulkUploadView.as_view(), name='teacher-upload'),
  path('downloadcsv/', downloadcsv, name='download-csv'),

]