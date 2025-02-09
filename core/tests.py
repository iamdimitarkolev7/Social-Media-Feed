from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Profile, FollowersCount

class UserViewsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Qwerty123')
        self.user2 = User.objects.create_user(username='testuser2', password='Qwerty123')
        self.profile = Profile.objects.create(user=self.user)
        self.post = Post.objects.create(user=self.user, content='Test post', created_at=timezone.now())
        self.client.login(username='testuser', password='Qwerty123')

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

        data = {'username': 'testuser', 'password': 'Qwerty123'}
        response = self.client.post(reverse('login'), data)
        self.assertRedirects(response, reverse('feed'))

    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

    def test_feed_view_authenticated(self):
        response = self.client.get(reverse('feed'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test post')

    def test_feed_view_guest(self):
        self.client.logout()
        response = self.client.get(reverse('feed'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test post')

    def test_post_create_view(self):
        response = self.client.get(reverse('post_create'))
        self.assertEqual(response.status_code, 200)

        data = {'content': 'New post content'}
        response = self.client.post(reverse('post_create'), data)
        self.assertRedirects(response, reverse('feed'))

        # Verify post is created
        post = Post.objects.get(content='New post content')
        self.assertEqual(post.content, 'New post content')

    def test_post_edit_view(self):
        response = self.client.get(reverse('post_edit', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)

        data = {'content': 'Updated post content'}
        response = self.client.post(reverse('post_edit', args=[self.post.id]), data)
        self.assertRedirects(response, reverse('feed'))

        # Verify post is updated
        post = Post.objects.get(id=self.post.id)
        self.assertEqual(post.content, 'Updated post content')

    def test_post_delete_view(self):
        response = self.client.get(reverse('post_delete', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('post_delete', args=[self.post.id]))
        self.assertRedirects(response, reverse('feed'))

        # Verify post is deleted
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(id=self.post.id)

    def test_like_post_view(self):
        response = self.client.get(reverse('like', args=[self.post.id]))
        self.assertRedirects(response, reverse('feed'))

        # Verify the post is liked
        self.assertIn(self.user, self.post.liked_posts.all())

    def test_user_profile_view(self):
        response = self.client.get(reverse('user_profile', args=[self.user.username]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test post')

    def test_follow_user_view(self):
        response = self.client.get(reverse('follow_user', args=[self.user2.username]))
        self.assertRedirects(response, reverse('user_profile', args=[self.user2.username]))

        # Verify follow relationship
        follow = FollowersCount.objects.get(follower=self.user, user=self.user2)
        self.assertIsNotNone(follow)

    def test_unfollow_user_view(self):
        # First, follow the user
        self.client.get(reverse('follow_user', args=[self.user2.username]))

        response = self.client.get(reverse('unfollow_user', args=[self.user2.username]))
        self.assertRedirects(response, reverse('user_profile', args=[self.user2.username]))

        # Verify unfollow relationship
        with self.assertRaises(FollowersCount.DoesNotExist):
            FollowersCount.objects.get(follower=self.user, user=self.user2)

    def test_search_users_view(self):
        response = self.client.get(reverse('search_users') + '?q=testuser2')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser2')

