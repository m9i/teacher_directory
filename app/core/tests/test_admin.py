from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from django.contrib.admin.options import ModelAdmin
from core.models import Teacher
from core.admin import TeacherAdmin


class MockRequest:
    pass


class MockSuperUser:
    def has_perm(self, perm, obj=None):
        return True


request = MockRequest()
request.user = MockSuperUser()


class ModelAdminTests(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        teacher_fields = {'first_name':'Tamela',
            'last_name':'Tomblin',
            'email':'teach1@school.com',
            'room':'2d',
            'phone': "+971-505-555-353",
            'subjects':'geography, Computer science, Biology, Chemistry',}  
        cls.teacher = Teacher.objects.create(**teacher_fields)

    def setUp(self):
        self.site = AdminSite()

    def test_modeladmin_str(self):
        ma = ModelAdmin(Teacher, self.site)
        self.assertEqual(str(ma), 'core.ModelAdmin')

    def test_default_fields(self):
        ma = ModelAdmin(Teacher, self.site)
        self.assertEqual(list(ma.get_fields(request)),
                        ['date_removed', 'is_active', 'email',
                          'first_name', 'last_name', 'phone', 'room',
                           'subjects', 'profile_pic','validation_error','is_valid'])
        self.assertEqual(list(ma.get_fields(request, self.teacher)),
                        ['date_removed', 'is_active', 'email',
                          'first_name', 'last_name', 'phone', 'room',
                           'subjects', 'profile_pic', 'validation_error','is_valid'])
        self.assertIsNone(ma.get_exclude(request, self.teacher))
    
    