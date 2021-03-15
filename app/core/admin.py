from django.contrib import admin
from imagekit.admin import AdminThumbnail

from .models import Teacher, TeacherBulkUpload


class TeacherAdmin(admin.ModelAdmin):
    # readonly_fields = ['get_photo_url',]
    search_fields = ['email', 
                     'first_name',
                     'last_name',
                     'phone',
                     'subjects',
                     ]
    list_display = ['email', 
                     'first_name',
                     'last_name',
                     'phone',
                     'subjects',
                     ]
    # fields = ['email', 
            #   'first_name',
            #   'last_name',
            #   'phone',
            #   'subjects',
            #   'get_photo_url',]
    
    
class TeacherBulkUploadAdmin(admin.ModelAdmin):
    pass


admin.site.register(Teacher, TeacherAdmin)
admin.site.register(TeacherBulkUpload, TeacherBulkUploadAdmin)