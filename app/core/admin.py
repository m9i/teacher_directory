from django.contrib import admin
from django import forms

from .models import Teacher, TeacherBulkUpload




class TeacherAdminForm(forms.ModelForm):
    class Meta:
        model = Teacher
        exclude = [id, ]

    def clean(self):
        subjects = self.cleaned_data.get('subjects')
        if subjects.split(',').__len__() > 5: 
            raise forms.ValidationError("Can't add more than 5 subjects to a Teacher")
        return self.cleaned_data

class TeacherAdmin(admin.ModelAdmin):
    form = TeacherAdminForm
    list_per_page = 15
    readonly_fields =['_validation_error',]
    search_fields = [
                     'last_name',
                     'subjects',
                     ]
    list_display = ['email', 
                     'first_name',
                     'last_name',
                     'phone',
                     'subjects',
                     '_validation_error',
                     ]
    fields = [( 
              'first_name',
              'last_name',
              'phone',
              'email',
              'subjects',
              'profile_pic',
              '_validation_error',)
                ]
    def _validation_error(self,instance):
        error = {'validation_error':"Can't add more than 5 subjects to a Teacher"}
        if instance.subjects.split(',').__len__() > 5: 
            instance.validation_error = error['validation_error']
            return instance.validation_error
    
class TeacherBulkUploadAdmin(admin.ModelAdmin):
    fields = [( 
              'csv_file',
              'image_zip_file',)
                ]
    

admin.site.register(Teacher, TeacherAdmin)
admin.site.register(TeacherBulkUpload, TeacherBulkUploadAdmin)