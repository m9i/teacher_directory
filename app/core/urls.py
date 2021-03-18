from django.urls import path

from .views import *


urlpatterns = [
  path('', IndexView.as_view(), name='home'),
#   path('list', search, name='search'),
  path('list', TeacherListView.as_view(), 
       name='teacher-list'),
#   path('list', result_view,
      #   name='result_detail_view'
#     ),
  path('<int:pk>/', TeacherDetailView.as_view(),
        name='teacher-detail'),
  path('create/', TeacherCreateView.as_view(),
        name='teacher-create'),
  path('<int:pk>/update/', TeacherUpdateView.as_view(),
        name='teacher-update'),
  path('delete/<int:pk>/', TeacherDeleteView.as_view(),
        name='teacher-delete'),
  path('upload/', TeacherBulkUploadView.as_view(),
        name='teacher-upload'),
  path('downloadcsv/', downloadcsv,
        name='download-csv'),
  

]

