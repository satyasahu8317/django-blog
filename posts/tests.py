from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post

class BlogTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password')
        # Create a test post
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            body='This is a short post for testing.',
            status='published'
        )

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'Test Post')
        self.assertEqual(f'{self.post.author}', 'testuser')
        self.assertEqual(self.post.body, 'This is a short post for testing.')

    def test_read_time_calculation(self):
        """Test if our read time logic works (under 200 words should be 1 min)"""
        self.assertEqual(self.post.get_read_time(), 1)

    def test_search_view(self):
        """Test if our search results actually find the post"""
        response = self.client.get('/search/?q=Test')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_post_detail_view(self):
        """Test if the detail page loads correctly"""
        response = self.client.get(f'/{self.post.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
