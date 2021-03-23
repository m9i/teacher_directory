from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from core.models import Subject, Teacher

class MockRequest:
    pass


class MockSuperUser:
    def has_perm(self, perm, obj=None):
        return True


request = MockRequest()
request.user = MockSuperUser()


class TeacherDirectoryTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        teacher_fields = {'first_name':'Tamela',
            'last_name':'Tomblin',
            'email':'teach1@school.com',
            'room':'2d',
            'phone': "+971-505-555-353",}
        sub_to_create = []
        subjects = ['geography', 'Computer science', 'Biology, Chemistry']
        cls.teacher = Teacher.objects.create(**teacher_fields)
        for i in  subjects:
            if not Subject.objects.filter(name=i.capitalize()).exists():
                subject = Subject.objects.create(name=i)
                cls.subjects = Teacher.subjects.through.objects.get_or_create(teacher_id=cls.teacher.id, 
                                                                              subject_id=subject.id)       
    
    def setUp(self):
        self.site = AdminSite()
        
    def tearDown(self):
        super().tearDown()
     
    def test_teacher_default_photo_url(self):
        self.assertEqual(self.teacher.get_photo_url(),
                         '/media/default-placeholder-image.png')
    
    def test_teacher_absolute_url(self):
        self.assertEqual(self.teacher.get_absolute_url(),'/core/1/')
    
    
    def test_first_name_max_length(self):
        max_length = self.teacher._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 255)

    def test_object_name_is_first_name_last_name_tupple_room(self):
        expected_object_name = f'{self.teacher.first_name} {self.teacher.last_name} ({self.teacher.room})'
        self.assertEqual(expected_object_name, str(self.teacher))
    



        
    
        

