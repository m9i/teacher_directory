from django import forms

from .models import Teacher

# A teacher can teach no more than 5 subjects
class TeacherForm(forms.ModelForm):
    """ 
    A teacher can teach no more than 5 subjects
    """
    class Meta:
        model = Teacher
        exclude = [id, 'date_removed', 'validation_error',]

    def clean(self):
        subjects = self.cleaned_data.get('subjects')
        if subjects.__len__() > 5: 
            raise forms.ValidationError("Can't add more than 5 subjects to a Teacher")
        return self.cleaned_data