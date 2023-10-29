import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from book_page.models import Book
from .models import Post, Reply
from .views import show_forum, get_posts_json, get_replies_json

class ForumViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', password='testpassword')

        self.post = Post.objects.create(user=self.user, subject='Test Subject', topic='Test Topic', message='Test Message')
        self.reply = Reply.objects.create(user=self.user, post=self.post, body='Test Reply')
        
        self.book1 = Book.objects.create(nama_buku='Book 1', genre_1='Genre A')
        self.book2 = Book.objects.create(nama_buku='Book 2', genre_1='Genre B')

    def test_main_using_main_template(self):
        response = Client().get('/forum/')
        self.assertTemplateUsed(response, 'forum.html')

    def test_show_forum_view_non_ajax(self):
        # Test the non-AJAX behavior of the show_forum view

        # Log in the test user
        self.client.login(username='testuser', password='testpassword')

        # Access the view without AJAX
        response = self.client.get(reverse('forum:show_forum'))

        self.assertEqual(response.status_code, 200)  # Expect a successful response

        # Check that the context data is correctly passed to the template
        self.assertIn('books', response.context)
        self.assertIn('user', response.context)
        self.assertIn('post', response.context)
        self.assertIn('all_genres', response.context)

        # Check the rendered template
        self.assertTemplateUsed(response, 'forum.html')

    def test_show_forum_view_ajax(self):
        # Test the AJAX behavior of the show_forum view

        # Create a request data dictionary to simulate an AJAX POST request
        ajax_request_data = {'selected_genre': 'Genre A'}

        # Access the view with AJAX and POST data
        response = self.client.post(reverse('forum:show_forum'), ajax_request_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)  # Expect a successful response

        # Parse the JSON response
        response_data = json.loads(response.content.decode('utf-8'))

        # Check the JSON response
        self.assertIn('topic_options', response_data)
        topic_options = response_data['topic_options']
        self.assertEqual(len(topic_options), 1)  # Expect one topic option
        self.assertEqual(topic_options[0]['value'], 'Book 1')
        self.assertEqual(topic_options[0]['text'], 'Book 1')

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

    def test_delete_post_view(self):
        # Test the delete_post view
        post_id = self.post.pk
        url = reverse('forum:delete_post', args=[post_id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)  # Expect a redirect (HTTP 302)

        # Check if the post is deleted
        with self.assertRaises(Post.DoesNotExist):
            post = Post.objects.get(pk=post_id)

    def test_delete_reply_view(self):
        # Test the delete_reply view
        reply_id = self.reply.pk
        url = reverse('forum:delete_reply', args=[reply_id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)  # Expect a redirect (HTTP 302)

        # Check if the reply is deleted
        with self.assertRaises(Reply.DoesNotExist):
            reply = Reply.objects.get(pk=reply_id)
            
    def test_add_post_view(self):
        # Simulate an AJAX POST request to add_post
        data = {
            'subject': 'Test Subject',
            'topic': 'Test Topic',
            'message': 'Test Message',
        }
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('forum:add_post'), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)  # Expect a successful response
        response_data = json.loads(response.content.decode('utf-8'))

        # Check the response JSON
        self.assertIn('fields', response_data)  # Check for the 'fields' key
        fields = response_data['fields']
        self.assertIn('user', fields)  # Check for the 'user' key within 'fields'
        self.assertIn('subject', fields)  # Check for the 'post' key within 'fields'
        self.assertIn('topic', fields)  # Check for the 'body' key within 'fields'
        self.assertIn('message', fields)  # Check for the 'body' key within 'fields'
        self.assertIn('date', fields)  # Check for the 'date' key within 'fields'

        # Verify that the post was created in the database
        self.assertTrue(Post.objects.filter(subject='Test Subject').exists())

    def test_add_reply_view(self):
        # Create a test post to reply to
        post = Post.objects.create(user=self.user, subject='Test Post', topic='Test Topic', message='Test Message')

        # Simulate an AJAX POST request to add_reply
        data = {
            'body': 'Test Reply',
        }
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('forum:add_reply', args=[post.pk]), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)  # Expect a successful response
        response_data = json.loads(response.content.decode('utf-8'))

        # Check the response JSON
        self.assertIn('fields', response_data)  # Check for the 'fields' key
        fields = response_data['fields']
        self.assertIn('user', fields)  # Check for the 'user' key within 'fields'
        self.assertIn('post', fields)  # Check for the 'post' key within 'fields'
        self.assertIn('body', fields)  # Check for the 'body' key within 'fields'
        self.assertIn('date', fields)  # Check for the 'date' key within 'fields'

        # Verify that the reply was created in the database
        self.assertTrue(Reply.objects.filter(body='Test Reply').exists())
