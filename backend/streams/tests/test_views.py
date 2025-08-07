# test_views.py (for DRF views if any)
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from streams.models import Stream


class StreamKeyViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_get_stream_key_authenticated(self):
        """Test getting stream key when authenticated"""
        self.client.force_authenticate(user=self.user)
        
        # Assuming you have a URL pattern for this view
        # You may need to adjust the URL name based on your urls.py
        url = reverse('streamkey')  # Adjust this to match your URL pattern
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('stream_key', response.data)
        
        # Verify stream was created
        stream = Stream.objects.get(user=self.user)
        self.assertEqual(response.data['stream_key'], stream.stream_key)
        
    def test_get_stream_key_unauthenticated(self):
        """Test getting stream key when not authenticated"""
        url = reverse('streamkey')  # Adjust this to match your URL pattern
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
