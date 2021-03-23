from django.contrib import admin
from django.db.models import Q

from .models import Subject, Teacher, TeacherBulkUpload
from .forms import TeacherForm


class SubjectInline(admin.TabularInline):
    model = Teacher.subjects.through
    extra = 0

class TeacherAdmin(admin.ModelAdmin):
    form = TeacherForm
    # inlines=[SubjectInline,]
    list_per_page = 15
    readonly_fields =['get_subjects',]
    search_fields = ['last_name','subjects__name',]
    list_display = ['email', 
                     'first_name',
                     'last_name',
                     'phone',
                     'get_subjects',
                     'is_valid',
                     ]
    fields = [( 
              'first_name',
              'last_name',
              'phone',
              'email',
              'subjects',
              'profile_pic',
              'is_valid',
              )
                ]
    # The directory should allow Teachers to filtered by first letter of last name or by subject.
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(
            TeacherAdmin, self).get_search_results(
                request, queryset, search_term)
        try:
            search_term_as_int = int(search_term)
            queryset |= self.model.objects.filter(
                Q(last_name__startwith=search_term_as_int)|
                 Q(subjects__name__startwith=search_term_as_int))
        except:
            pass
        return queryset, use_distinct
    
class TeacherBulkUploadAdmin(admin.ModelAdmin):
    fields = [( 
              'csv_file',
              'image_zip_file',)
                ]
    

class SubjectAdmin(admin.ModelAdmin):
    list_per_page = 15
    search_fields = ['name',]
    

admin.site.register(Teacher, TeacherAdmin)
admin.site.register(TeacherBulkUpload, TeacherBulkUploadAdmin)
admin.site.register(Subject, SubjectAdmin)