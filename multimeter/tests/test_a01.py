""" Тест по карточке A-01 Создание и редактирование задач
Автор может создавать, просматривать, редактировать и удалять задачи.
Автор должен указать её название.
Автор может указать теги для быстрого поиска.
Система должна автоматически фиксировать дату её модификации. """

from django.test import TestCase
from django.utils.timezone import now

from multimeter import models


class TestA01(TestCase):
    """ Тестирование представлений (views) учетной записи """

    def setUp(self):
        self.author = models.Account()
        self.author.is_staff = True
        self.author.username = 'author'
        self.author.set_password('password')
        self.author.save()

        self.problem = models.Problem()
        self.problem.codename = 'Problem 1'
        self.problem.author = self.author
        self.problem.time_limit = 1000
        self.problem.memory_limit = 64
        self.problem.save()

        self.tag1 = models.Tag()
        self.tag1.tag = 'tag1'
        self.tag1.save()
        self.tag1.problems.add(self.problem)  # pylint: disable=no-member

        self.tag2 = models.Tag()
        self.tag2.tag = 'tag2'
        self.tag2.save()

    def test_problem_create(self):
        """ Проверка создания задачи """
        self.client.login(username='author', password='password')

        response = self.client.get('/ru/problem/create/')
        self.assertEqual(200, response.status_code)
        self.assertContains(response, 'Редактирование задачи')
        self.assertContains(response, 'Кодовое название')
        self.assertContains(response, 'Теги')
        self.assertContains(response, 'Сохранить')

        time1 = now()
        response = self.client.post('/ru/problem/create/', {
            'codename': 'Problem 2',
            'tags': 'tag1 tag3',
            'time_limit': 1000,
            'memory_limit': 64,
            'author': self.author.id,
        })
        time2 = now()
        self.assertEqual(302, response.status_code)

        created_problem = models.Problem.objects.get(codename='Problem 2')
        tags = [t.tag for t in created_problem.tags.all()]
        self.assertIn('tag1', tags)
        self.assertIn('tag3', tags)
        self.assertEqual(1000, created_problem.time_limit)
        self.assertEqual(64, created_problem.memory_limit)
        self.assertEqual(self.author, created_problem.author)
        self.assertLessEqual(time1, created_problem.last_modified)
        self.assertGreaterEqual(time2, created_problem.last_modified)

    def test_problem_list(self):
        """ Проверка списка задач """
        self.client.login(username='author', password='password')

        response = self.client.get('/ru/problem/list/')
        self.assertEqual(200, response.status_code)
        self.assertContains(response, 'Problem 1')
        self.assertContains(response, 'author')
        self.assertContains(response, 'Создать')

    def test_problem_update(self):
        """ Проверка изменения задачи """
        self.client.login(username='author', password='password')

        response = self.client.get('/ru/problem/update/%d/' % self.problem.id)
        self.assertEqual(200, response.status_code)
        self.assertContains(response, 'Problem 1')
        self.assertContains(response, 'tag1')

        time1 = now()
        response = self.client.post('/ru/problem/update/%d/' % self.problem.id, {
            'codename': 'Problem 2',
            'tags': 'tag1 tag2',
            'time_limit': 1000,
            'memory_limit': 64,
            'author': self.author.id,
        })
        time2 = now()
        self.assertEqual(302, response.status_code)

        updated_problem = models.Problem.objects.get(codename='Problem 2')
        tags = [t.tag for t in updated_problem.tags.all()]
        self.assertIn('tag1', tags)
        self.assertIn('tag2', tags)
        self.assertNotIn('tag3', tags)
        self.assertEqual(1000, updated_problem.time_limit)
        self.assertEqual(64, updated_problem.memory_limit)
        self.assertEqual(self.author, updated_problem.author)
        self.assertLessEqual(time1, updated_problem.last_modified)
        self.assertGreaterEqual(time2, updated_problem.last_modified)
