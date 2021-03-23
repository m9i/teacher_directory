from django import forms
from django.core.exceptions import ValidationError
from django.forms import ValidationError as FormValidationError

from .models import Subject, Teacher

# A teacher can teach no more than 5 subjects

class SubjectInlineForm(forms.ModelForm):
    
    subjects = forms.ModelChoiceField(queryset=Subject.objects.all())
    
    class Meta:
        model = Teacher.subjects.through
        fields = '__all__'
    
    
    def __init__(self, *args, **kwargs):
        super(SubjectInlineForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance'):
            teacher = Teacher.objects.get(id=self.instance.id)
            self.fields['subjects'].initial = teacher.subjects
            
    def save(self, commit=True):
        instance = super(SubjectInlineForm, self).save(commit=False)
        teacher = Teacher.objects.get(id=instance.id)
        teacher.subjects = self.cleaned_data['subjects']
        teacher.save()

        if commit:
            instance.save()
        return instance
    
    def clean(self):
        super(SubjectInlineForm, self).clean(*args, **kwargs)
        teacher = Teacher.objects.get(id=instance.id)
        teacher.subjects = self.cleaned_data['subjects']
        if teacher.subjects.__len__() > 5: 
            raise FormValidationError("Can't add more than 5 subjects to a Teacher")
        return self.cleaned_data
    
class TeacherForm(forms.ModelForm):
    """ 
    A teacher can teach no more than 5 subjects 
    """    
    class Meta:
        model = Teacher
        exclude = [id, 'date_removed',]


    def clean_subjects(self):
        subjects = self.cleaned_data.get('subjects')
        if subjects.__len__() > 5: 
            raise FormValidationError("Can't add more than 5 subjects to a Teacher")
        return subjects