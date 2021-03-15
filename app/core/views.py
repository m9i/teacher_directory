import csv
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.forms import widgets
from django.urls import reverse_lazy

from .models import Teacher, TeacherBulkUpload


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'


@login_required
def teacher_list(request):
  teachers = Teacher.objects.all()
  return render(request, 'core/teacher_list.html', {"teachers":teachers})


class TeacherDetailView(LoginRequiredMixin, DetailView):
    model = Teacher
    template_name = "core/teacher_detail.html"

    def get_context_data(self, **kwargs):
        context = super(TeacherDetailView, self).get_context_data(**kwargs)
        return context


class TeacherCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Teacher
    fields = '__all__'
    success_message = "New teacher successfully added."

    def get_form(self):
        '''add date picker in forms'''
        form = super(TeacherCreateView, self).get_form()
        form.fields['email'].widget = widgets.Textarea(attrs={'rows': 2})
        form.fields['phone'].widget = widgets.Textarea(attrs={'rows': 2})
        return form


class TeacherUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Teacher
    fields = '__all__'
    success_message = "Record successfully updated."

    def get_form(self):
        '''add date picker in forms'''
        form = super(TeacherUpdateView, self).get_form()
        form.fields['email'].widget = widgets.Textarea(attrs={'rows': 2})
        form.fields['room'].widget = widgets.Textarea(attrs={'rows': 2})
        form.fields['profile_pic'].widget = widgets.FileInput()
        return form


class TeacherDeleteView(LoginRequiredMixin, DeleteView):
    model = Teacher
    success_url = reverse_lazy('teacher-list')


class TeacherBulkUploadView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = TeacherBulkUpload
    template_name = 'core/teacher_upload.html'
    fields = ['csv_file']
    success_url = '/list'
    success_message = 'Successfully uploaded teachers'

@login_required
def downloadcsv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="teacher_template.csv"'

    writer = csv.writer(response)
    writer.writerow(['First Name', 'Last Name',
                     'Email Adress', 'Room Number',
                     'Phone Number', 'Subjects taught'])

    return response