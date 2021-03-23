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
  path('<int:pk>/', teacher_detail,
        name='teacher-detail'),
  path('create/', teacher_create,
        name='teacher-create'),
  path('<int:pk>/update/', teacher_update,
        name='teacher-update'),
  path('delete/<int:pk>/', teacher_delete,
        name='teacher-delete'),
  path('upload/', bulkupload_teacher,
        name='teacher-upload'),
  path('downloadcsv/', downloadcsv,
        name='download-csv'),
  
  path('create_subject',
        create_subject,
        name='create_subject'
    ),
  path('subjects/',
        subject_list,
        name='subject_list'),
]

