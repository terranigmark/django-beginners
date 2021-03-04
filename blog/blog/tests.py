from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Post
# from datetime import date

# Create your tests here.
class BlogTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = 'testuser',
            email = 'test@email.com',
            password = 'secret'
        )

        self.post = Post.objects.create(
            title = 'Awesome title!',
            body = 'Greate content for a great blog.',
            author = self.user,
            # publish_date = date.today()
        )

    def test_string_representation(self):
        post = Post(title = 'A sample title')
        self.assertEqual(str(post), post.title)

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'Awesome title!')
        self.assertEqual(f'{self.post.author}', 'testuser')
        self.assertEqual(f'{self.post.body}', 'Greate content for a great blog.')
        # self.assertEqual(f'{self.post.publish_date}', date.today().strftime('%Y-%m-%d'))

    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Greate content for a great blog.')
        self.assertTemplateUsed(response, 'home.html')

    def test_post_detail_view(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/3/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Awesome title!')
        self.assertTemplateUsed(response, 'post_detail.html')