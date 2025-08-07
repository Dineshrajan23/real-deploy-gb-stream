import uuid
from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError
from streams.models import Stream, Recording, generate_stream_key


class StreamModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_create_stream(self):
        """Test creating a stream with default values"""
        stream = Stream.objects.create(user=self.user, title='Test Stream')
        
        self.assertEqual(stream.user, self.user)
        self.assertEqual(stream.title, 'Test Stream')
        self.assertIsNotNone(stream.stream_key)
        self.assertEqual(len(stream.stream_key), 32)
        self.assertFalse(stream.is_live)
        self.assertIsNone(stream.hls_url)
        self.assertIsNotNone(stream.created_at)
        
    def test_generate_stream_key(self):
        """Test stream key generation"""
        key = generate_stream_key()
        self.assertEqual(len(key), 32)
        self.assertIsInstance(key, str)
        
    def test_unique_stream_key(self):
        """Test that stream keys are unique"""
        stream1 = Stream.objects.create(user=self.user, title='Stream 1')
        
        # Create another user
        user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com', 
            password='testpass123'
        )
        stream2 = Stream.objects.create(user=user2, title='Stream 2')
        
        self.assertNotEqual(stream1.stream_key, stream2.stream_key)
        
    def test_one_to_one_relationship(self):
        """Test that a user can only have one stream"""
        Stream.objects.create(user=self.user, title='First Stream')
        
        # Creating another stream for the same user should raise an error
        with self.assertRaises(IntegrityError):
            Stream.objects.create(user=self.user, title='Second Stream')
            
    def test_stream_str_method(self):
        """Test the string representation of Stream"""
        stream = Stream.objects.create(user=self.user, title='Test Stream')
        self.assertEqual(str(stream), 'testuser')


class RecordingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.stream = Stream.objects.create(user=self.user, title='Test Stream')
        
    def test_create_recording(self):
        """Test creating a recording"""
        recording = Recording.objects.create(
            stream=self.stream,
            file_path='/path/to/recording.mp4'
        )
        
        self.assertEqual(recording.stream, self.stream)
        self.assertEqual(recording.file_path, '/path/to/recording.mp4')
        self.assertIsNotNone(recording.created_at)
        
    def test_recording_str_method(self):
        """Test the string representation of Recording"""
        recording = Recording.objects.create(
            stream=self.stream,
            file_path='/path/to/recording.mp4'
        )
        
        str_repr = str(recording)
        self.assertIn('testuser', str_repr)
        self.assertIn('Recording for', str_repr)