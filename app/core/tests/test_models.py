from django.test import TestCase

from core.models import Teacher


class TeacherDirectoryTests(TestCase):
    def test_create_teacher(self):
        Teacher.objects.create(
            first_name = 'Tamela',
            last_name = 'Tomblin',
            email = 'teach1@school.com',
            room = '2d',
            phone = "+971-505-555-353",
            subjects = 'geography, Computer science, Biology, Chemistry',  
        )
        

