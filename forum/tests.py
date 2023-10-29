from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Reply
from .views import show_forum, get_posts_json, get_replies_json

class ForumViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', password='testpassword')

        self.post = Post.objects.create(user=self.user, subject='Test Subject', topic='Test Topic', message='Test Message')
        self.reply = Reply.objects.create(user=self.user, post=self.post, body='Test Reply')

    def test_main_using_main_template(self):
        response = Client().get('/forum/')
        self.assertTemplateUsed(response, 'forum.html')

    def test_get_posts_json_view(self):
        response = Client().get(reverse('forum:get_posts'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), [
            {
                "pk": self.post.pk,
                "fields": {
                    "user": self.user.username,
                    "subject": self.post.subject,
                    "topic": self.post.topic,
                    "message": self.post.message,
                    "date": self.post.date.strftime("%H:%M %Z - %B %d, %Y")
                }
            }
        ])

    def test_get_replies_json_view(self):
        post_id = self.post.pk
        response = self.client.get(reverse('forum:get_replies', args=[post_id]))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), [
            {
                "pk": self.reply.pk,
                "fields": {
                    "user": self.user.username,
                    "post": self.reply.post.id,
                    "body": self.reply.body,
                    "date": self.reply.date.strftime("%H:%M %Z - %B %d, %Y")
                }
            }
        ])
