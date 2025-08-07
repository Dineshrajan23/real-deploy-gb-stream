# backend/streams/tests/test_services.py
from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import Mock, patch
from streams.models import Stream, Recording
from streams.services import StreamManagementService, UserManagementService


class StreamManagementServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_get_stream_for_user_existing(self):
        """Test getting an existing stream for a user"""
        existing_stream = Stream.objects.create(user=self.user, title='Existing Stream')
        
        stream = StreamManagementService.get_stream_for_user(self.user)
        
        self.assertEqual(stream, existing_stream)
        self.assertEqual(Stream.objects.filter(user=self.user).count(), 1)
        
    def test_get_stream_for_user_new(self):
        """Test creating a new stream for a user"""
        stream = StreamManagementService.get_stream_for_user(self.user)
        
        self.assertIsNotNone(stream)
        self.assertEqual(stream.user, self.user)
        self.assertEqual(Stream.objects.filter(user=self.user).count(), 1)
        
    def test_update_stream_title_success(self):
        """Test updating stream title successfully"""
        Stream.objects.create(user=self.user, title='Old Title')
        
        updated_stream = StreamManagementService.update_stream_title(self.user, 'New Title')
        
        self.assertIsNotNone(updated_stream)
        self.assertEqual(updated_stream.title, 'New Title')
        
    def test_update_stream_title_no_stream(self):
        """Test updating stream title when no stream exists"""
        result = StreamManagementService.update_stream_title(self.user, 'New Title')
        
        self.assertIsNone(result)
        
    @patch('streams.services.rtmp_api_client')
    def test_reset_stream_key_success(self, mock_rtmp_client):
        """Test resetting stream key successfully"""
        stream = Stream.objects.create(user=self.user, title='Test Stream')
        old_key = stream.stream_key
        
        mock_rtmp_client.delete_stream.return_value = True
        mock_rtmp_client.add_stream.return_value = True
        
        updated_stream = StreamManagementService.reset_stream_key(self.user)
        
        self.assertIsNotNone(updated_stream)
        self.assertNotEqual(updated_stream.stream_key, old_key)
        mock_rtmp_client.delete_stream.assert_called_once_with(old_key)
        mock_rtmp_client.add_stream.assert_called_once_with(updated_stream.stream_key)
        
    def test_reset_stream_key_no_stream(self):
        """Test resetting stream key when no stream exists"""
        result = StreamManagementService.reset_stream_key(self.user)
        
        self.assertIsNone(result)
        
    def test_get_all_recordings(self):
        """Test getting all recordings"""
        stream = Stream.objects.create(user=self.user, title='Test Stream')
        recording1 = Recording.objects.create(stream=stream, file_path='/path1.mp4')
        recording2 = Recording.objects.create(stream=stream, file_path='/path2.mp4')
        
        recordings = StreamManagementService.get_all_recordings()
        
        self.assertEqual(len(recordings), 2)
        # Should be ordered by created_at descending
        self.assertEqual(recordings[0], recording2)
        self.assertEqual(recordings[1], recording1)
        
    def test_get_recording_by_id_exists(self):
        """Test getting a recording by ID that exists"""
        stream = Stream.objects.create(user=self.user, title='Test Stream')
        recording = Recording.objects.create(stream=stream, file_path='/path.mp4')
        
        result = StreamManagementService.get_recording_by_id(recording.id)
        
        self.assertEqual(result, recording)
        
    def test_get_recording_by_id_not_exists(self):
        """Test getting a recording by ID that doesn't exist"""
        result = StreamManagementService.get_recording_by_id(999)
        
        self.assertIsNone(result)
        
    def test_get_live_streams(self):
        """Test getting live streams"""
        # Create live stream
        live_stream = Stream.objects.create(user=self.user, title='Live Stream', is_live=True)
        
        # Create offline stream
        user2 = User.objects.create_user(username='user2', email='test2@example.com')
        Stream.objects.create(user=user2, title='Offline Stream', is_live=False)
        
        live_streams = StreamManagementService.get_live_streams()
        
        self.assertEqual(len(live_streams), 1)
        self.assertEqual(live_streams[0], live_stream)


class UserManagementServiceTest(TestCase):
    def test_register_user_success(self):
        """Test successful user registration"""
        user = UserManagementService.register_user(
            username='newuser',
            email='new@example.com',
            password='newpass123'
        )
        
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'new@example.com')
        # Check that a stream was created
        self.assertTrue(hasattr(user, 'stream'))
        
    def test_register_user_duplicate_username(self):
        """Test registering user with duplicate username"""
        User.objects.create_user(username='existing', email='existing@example.com')
        
        user = UserManagementService.register_user(
            username='existing',
            email='new@example.com',
            password='newpass123'
        )
        
        self.assertIsNone(user)