import csv
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import widgets
from django.urls import reverse_lazy

from .models import Teacher, TeacherBulkUpload
from .filters import TeacherFilter
from .permission_handlers import user_is_verified



class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'


def search(request):
    teacher = Teacher.objects.all()
    teacher_filter = TeacherFilter(request.GET, queryset=teacher)
    return render(request, 'core/teacher_list.html', {'filter': teacher_filter})

class TeacherListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Teacher
    template_name = 'core/teacher_list.html'
    
    def post(self, request, *args, **kwargs):
        teacher = Teacher.objects.all()
        teacher_filter = TeacherFilter(request.GET, queryset=teacher)
        return render(request, 'core/teacher_list.html', {'filter': teacher_filter})

    def test_func(self):
        user = self.request.user
        return user_is_verified(user)

    def get_queryset(self):
        queryset = Teacher.objects.all()
        return queryset
    
    def get_context_data(self, *args, object_list=None, **kwargs):
        ctx = super().get_context_data(*args, object_list=object_list, **kwargs)
        teachers = Teacher.objects.all()
        f = TeacherFilter(self.request.GET, queryset=teachers)
        ctx['filter'] = f
        return ctx


@user_passes_test(user_is_verified)
def result_view(request):
    if not request.GET:
        qs =  Teacher.objects.none()
    else:
        qs =  Teacher.objects.all()
    f = TeacherFilter(request.GET, queryset=qs)
    ctx = {'filter': f, }
    return render(request, 'result/teacher_list.html', ctx)


class TeacherDetailView(LoginRequiredMixin, DetailView):
    model = Teacher
    template_name = "core/teacher_detail.html"

    def get_context_data(self, **kwargs):
        context = super(TeacherDetailView, self).get_context_data(**kwargs)
        return context


class TeacherCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Teacher
    fields = ['first_name','last_name','email','phone','room','subjects','profile_pic']
    success_message = "New teacher successfully added."

    def get_form(self):
        '''add date picker in forms'''
        form = super(TeacherCreateView, self).get_form()
        form.fields['email'].widget = widgets.Textarea(attrs={'rows': 2})
        form.fields['phone'].widget = widgets.Textarea(attrs={'rows': 2})
        form.fields['profile_pic'].required = False
        return form


class TeacherUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Teacher
    fields = ['first_name','last_name','email','phone','room','subjects','profile_pic']
    success_message = "Record successfully updated."

    def get_form(self):
        '''add date picker in forms'''
        form = super(TeacherUpdateView, self).get_form()
        form.fields['email'].widget = widgets.Textarea(attrs={'rows': 2})
        form.fields['room'].widget = widgets.Textarea(attrs={'rows': 2})
        form.fields['profile_pic'].required = False
        form.fields['profile_pic'].widget = widgets.FileInput()
        return form


class TeacherDeleteView(LoginRequiredMixin, DeleteView):
    model = Teacher
    success_url = reverse_lazy('teacher-list')
    


class TeacherBulkUploadView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = TeacherBulkUpload
    template_name = 'core/teacher_upload.html'
    fields = ['csv_file']
    success_url = reverse_lazy('teacher-list')
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