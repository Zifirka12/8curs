
from urllib import request, response
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.serializers import ValidationError

from materials.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email='meow@meow.meow')
        self.client.force_authenticate(user=self.user)
        self.lesson = Lesson.objects.create(name='test1', owner=self.user)

    def test_create_lesson(self):
        data = {
            'name': 'test', }
        response = self.client.post('/lesson/create/', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.json(),
                        {"id": 2,
                         "name": "test",
                         "description": None,
                         "preview": None,
                         "video": None,
                         "course": None,
                         "owner": self.user})

    def test_create_lesson_failed(self):
        data = {
            'name': 'test',
            'video': 'https://my.sky.pro/'}
        response = self.client.post('/lesson/create/', data=data)

        self.assertRaises(ValidationError)

    def test_view_lessons(self):
        response = self.client.get('/lesson/')
        response1 = self.client.get(f'/lesson/{self.lesson.pk}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

    def test_view_lesson_failed(self):
        response = self.client.get(f'/lesson/0')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_lesson(self):
        data = {
            'name': 'test1',
            'description': 'test',
        }
        response = self.client.put(f'/lesson/update/{self.lesson.pk}', data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json(),
                        {"id": self.lesson.pk,
                         "name": "test1",
                         "description": "test",
                         "preview": None,
                         "video": None,
                         "course": None,
                         "owner": self.user})

    def test_delete_lesson(self):
        response = self.client.delete(f'/lesson/delete/{self.lesson.pk}')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_lesson_failed(self):
        response = self.client.delete(f'/lesson/delete/0')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SubTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='meow@meow.meow')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name='test')

    def test_subscription(self):
        data = {
            'course_id': self.course.pk
        }
        response = self.client.post(f'/courses/{self.course.pk}/subscribe', data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "подписка добавлена"})

        response1 = self.client.post(f'/courses/{self.course.pk}/subscribe', data=data)

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.json(), {"message": "подписка удалена"})