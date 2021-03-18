from django.contrib import admin
from django import forms
from django.db.models import Q

from .models import Teacher, TeacherBulkUpload


class TeacherAdminForm(forms.ModelForm):
    class Meta:
        model = Teacher
        exclude = [id, ]

    def clean(self):
        difference = []
        subjects = self.cleaned_data.get('subjects')
        if set(subjects.split(',')).__len__() > 5: 
            raise forms.ValidationError("Can't add more than 5 subjects to a Teacher")
        return self.cleaned_data

class TeacherAdmin(admin.ModelAdmin):
    form = TeacherAdminForm
    list_per_page = 15
    readonly_fields =['get_validation_error',]
    search_fields = ['last_name','subjects',]
    list_display = ['email', 
                     'first_name',
                     'last_name',
                     'phone',
                     'subjects',
                     'get_validation_error',
                     'is_valid',
                     ]
    fields = [( 
              'first_name',
              'last_name',
              'phone',
              'email',
              'subjects',
              'profile_pic',
              'get_validation_error',
              'is_valid',
              )
                ]
    
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(TeacherAdmin, self).get_search_results(request, queryset, search_term)
        try:
            search_term_as_int = int(search_term)
            queryset |= self.model.objects.filter(Q(last_name__startwith=search_term_as_int)| Q(subjects__startwith=search_term_as_int))
        except:
            pass
        return queryset, use_distinct
    
class TeacherBulkUploadAdmin(admin.ModelAdmin):
    fields = [( 
              'csv_file',
              'image_zip_file',)
                ]
    

admin.site.register(Teacher, TeacherAdmin)
admin.site.register(TeacherBulkUpload, TeacherBulkUploadAdmin)