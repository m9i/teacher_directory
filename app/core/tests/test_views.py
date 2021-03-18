from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User

import unittest
from django.test import Client
from django.urls import reverse

from core.models import Teacher

class MockRequest:
    pass


class MockSuperUser:
    def has_perm(self, perm, obj=None):
        return True


request = MockRequest()
request.user = MockSuperUser()


class TeacherListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_teachers = 13

        for teacher_id in range(number_of_teachers):
            Teacher.objects.create(
                first_name=f'FirstName{teacher_id}',
                last_name=f'LastName{teacher_id}',
                email=f'teach{teacher_id}@school.com',
            )
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()
        self.user = User.objects.create_user(username='Foo',
                                              password='barbaz',
                                              is_superuser=True,
                                              is_staff=True)
        self.factory = RequestFactory()
        

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('teacher-detail', 
                                           args=[1]), follow=True)
        self.assertEqual(response.status_code, 200)
 
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('teacher-list'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/login.html')
 
    def test_pagination_is_ten(self):
        response = self.client.get(reverse('teacher-detail',args=[2]),follow=True)
        self.assertEqual(response.status_code, 200)


    def test_lists_all_teachers(self):
        response = self.client.get(reverse('teacher-list')+'?page=2',follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('teacher-list'), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/core/list')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('teacher-list'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'core/teacher_list.html')