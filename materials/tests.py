from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework import status

from materials.models import Course, Lesson, Subscribe
from materials.views import LessonViewSet, SubscribeView

User = get_user_model()


class LessonViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = LessonViewSet.as_view({
            'get': 'list',
            'post': 'create',
            'delete': 'destroy',
        })
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client()
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        """ Test that a lesson can be created. """
        course = Course.objects.create(name='Test Course', owner=self.user)
        data = {'name': 'Test Lesson', 'course': course.id}
        request = self.factory.post('/lessons/', data, format='json')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)
        self.assertEqual(Lesson.objects.get().name, 'Test Lesson')

    def test_delete_lesson(self):
        """ Test that a lesson can be deleted. """
        course = Course.objects.create(name='Test Course', owner=self.user)
        lesson = Lesson.objects.create(name='Test Lesson', course=course, owner=self.user)
        data = {'course': course.id, 'lesson': lesson.id}
        request = self.factory.delete('/lessons/', data, format='json')
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=lesson.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)


class SubscribeViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = SubscribeView.as_view()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client()
        self.client.force_authenticate(user=self.user)

    def test_subscribe(self):
        """ Test that a user can subscribe to a course. """
        course = Course.objects.create(name='Test Course', owner=self.user)
        data = {'course_id': course.id}
        request = self.factory.post('/subscribe/', data, format='json')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscribe.objects.count(), 1)
        self.assertEqual(Subscribe.objects.get().user, self.user)
        self.assertEqual(Subscribe.objects.get().course, course)

    def test_unsubscribe(self):
        """ Test that a user can unsubscribe from a course. """
        course = Course.objects.create(name='Test Course', owner=self.user)
        Subscribe.objects.create(user=self.user, course=course)
        data = {'course_id': course.id}
        request = self.factory.post('/subscribe/', data, format='json')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscribe.objects.count(), 0)
