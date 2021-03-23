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
from django.template import RequestContext


from .models import Subject, Teacher, TeacherBulkUpload
from .filters import TeacherFilter, SubjectFilter
from .permission_handlers import user_is_verified
from .forms import TeacherForm



def handler404(request, *args, **argv):
    error = 'Request Not Found, back to previous page!'
    response = render(request, 'core/error_page.html', {})
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    error = 'Server Is Busy, try later!'
    response = render(request, 'core/error_page.html', {})
    response.status_code = 500
    return response


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'core/index.html'


def search(request):
    teacher = Teacher.objects.all()
    teacher_filter = TeacherFilter(request.GET, queryset=teacher)
    return render(request, 'core/teacher_list.html', {'filter': teacher_filter})

class TeacherListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Teacher
    template_name = 'core/teacher_list.html'
    paginate_by = 10
    
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

teacher_detail = TeacherDetailView.as_view()

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

teacher_create = TeacherCreateView.as_view()

class TeacherUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Teacher
    # fields = ['first_name','last_name','email','phone','room','subjects','profile_pic']
    success_message = "Record successfully updated."
    form_class = TeacherForm
    
    def form_valid(self, form):
        update_subjects = form.save(commit=False)
        update_subjects.save()
        form.save_m2m()
        return super(TeacherUpdateView, self).form_valid(form)
    
teacher_update = TeacherUpdateView.as_view()

class TeacherDeleteView(LoginRequiredMixin, DeleteView):
    model = Teacher
    success_url = reverse_lazy('teacher-list')
    
teacher_delete = TeacherDeleteView.as_view()

class TeacherBulkUploadView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = TeacherBulkUpload
    template_name = 'core/teacher_upload.html'
    fields = ['csv_file', 'image_zip_file']
    success_url = reverse_lazy('teacher-list')
    success_message = 'Successfully uploaded teachers'

bulkupload_teacher = TeacherBulkUploadView.as_view()

class SubjectListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Subject
    context_object_name = 'subjects'
    template_name = 'core/subject_list.html'
    paginate_by = 10

    def test_func(self):
        user = self.request.user
        return user_is_verified(user)
    
    def post(self, request, *args, **kwargs):
        subject = Subject.objects.all()
        subject_filter = SubjectFilter(request.GET, queryset=subject)
        return render(request, 'core/subject_list.html', {'filter': subject_filter})


    def get_queryset(self):
        queryset = Subject.objects.all()
        return queryset
    
    def get_context_data(self, *args, object_list=None, **kwargs):
        ctx = super().get_context_data(*args, object_list=object_list, **kwargs)
        subjects = Subject.objects.all()
        f = SubjectFilter(self.request.GET, queryset=subjects)
        ctx['filter'] = f
        return ctx

subject_list = SubjectListView.as_view()


class CreateSubjectView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Subject
    fields = ['name',]
    template_name = 'core/subject_create.html'
    success_url = reverse_lazy('subject_list')

    def test_func(self):
        user = self.request.user
        return user_is_verified(user)
    

    
create_subject = CreateSubjectView.as_view()


@login_required
def downloadcsv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="teacher_template.csv"'

    writer = csv.writer(response)
    writer.writerow(['First Name', 'Last Name',
                     'Email Adress', 'Room Number',
                     'Phone Number', 'Subjects taught'])

    return response

