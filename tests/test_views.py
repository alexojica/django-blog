from django.test import RequestFactory, TestCase
from hello import views
from django.contrib.auth.models import AnonymousUser, User
from django.core.exceptions import PermissionDenied
from hello.forms import PostForm


class AddPostViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@abc.com', password='top_secret')

    def test_add_post_view_success_status_code_authenticated_user(self):
        request = self.factory.post('/add')
        request.user = self.user
        response = views.add_post(request)
        self.assertEquals(response.status_code, 302)

    def test_add_post_view_redirects_on_success(self):
        data = {
            'title': 'Test title',
            'text': 'Test text',
        }
        request = self.factory.post('/add', data)
        request.user = self.user
        response = views.add_post(request)
        self.assertEqual(response.get('location'), '/post_list/')

    def test_add_post_view_form_invalid(self):
        request = self.factory.post('/add', {})
        request.user = self.user
        response = views.add_post(request)
        self.assertEquals(response.status_code, 200)

    def test_add_post_view_anonymous_user(self):
        request = self.factory.post('/add')
        request.user = AnonymousUser()
        with self.assertRaises(PermissionDenied):
            views.add_post(request)

    def test_add_post_view_post_form(self):
        request = self.factory.get('/add')
        request.user = AnonymousUser()
        response = views.add_post(request)
        self.assertIsInstance(response.context_data['form'], PostForm)
