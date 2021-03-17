from django.test import TestCase

from core.models import Teacher


class TeacherDirectoryTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        teacher_fields = {'first_name':'Tamela',
            'last_name':'Tomblin',
            'email':'teach1@school.com',
            'room':'2d',
            'phone': "+971-505-555-353",
            'subjects':'geography, Computer science, Biology, Chemistry',}  
        Teacher.objects.create(**teacher_fields)        

    def tearDown(self):
        pass
     
    def test_teacher_default_photo_url(self):
        teacher=Teacher.objects.get(id=1)
        self.assertEqual(teacher.get_photo_url(),
                         '/media/default-placeholder-image.png')
    
    def test_teacher_absolute_url(self):
        teacher=Teacher.objects.get(id=1)
        self.assertEqual(teacher.get_absolute_url(),'/core/1/')
    
    
    def test_first_name_max_length(self):
        teacher=Teacher.objects.get(id=1)
        max_length = teacher._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 255)

    def test_object_name_is_first_name_last_name_tupple_room(self):
        teacher=Teacher.objects.get(id=1)
        expected_object_name = f'{teacher.first_name} {teacher.last_name} ({teacher.room})'
        self.assertEqual(expected_object_name, str(teacher))
    
    def test_get_validation_error_none(self):
        teacher=Teacher.objects.get(id=1)
        self.assertEqual(teacher.get_validation_error(), None)
    
    def test_get_validation_error(self):
        subjects='geography, Computer science, Biology, Chemistry, English, Mathematics'
        teacher=Teacher.objects.get(id=1)
        teacher.subjects = subjects
        self.assertEqual(teacher.get_validation_error(),
                          "Can't add more than 5 subjects to a Teacher and now is 6")
        
    
        

