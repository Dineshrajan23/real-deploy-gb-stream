from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import patch, Mock, PropertyMock
from ninja.testing import TestClient
from streams.api import api
from streams.models import Stream, Recording


class APITestCase(TestCase):
    def setUp(self):
        self.client = TestClient(api)
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_get_csrf_cookie(self):
        """Test getting CSRF cookie"""
        response = self.client.get("/csrf-cookie")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"detail": "CSRF cookie set"})
        
    def test_login_valid_credentials(self):
        """Test login with valid credentials"""
        response = self.client.post("/login", json={
            "username": "testuser",
            "password": "testpass123"
        })
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["username"], "testuser")
        
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post("/login", json={
            "username": "testuser",
            "password": "wrongpass"
        })
        
        self.assertEqual(response.status_code, 401)
        data = response.json()
        self.assertFalse(data["success"])
        
    def test_register_new_user(self):
        """Test registering a new user"""
        with patch('streams.api.UserManagementService.register_user') as mock_register:
            mock_user = Mock()
            mock_user.username = 'newuser'
            mock_register.return_value = mock_user
            
            response = self.client.post("/register", json={
                "username": "newuser",
                "email": "new@example.com",
                "password": "newpass123"
            })
            
            self.assertEqual(response.status_code, 201)
            data = response.json()
            self.assertTrue(data["success"])
            self.assertEqual(data["username"], "newuser")
            
    def test_register_existing_user(self):
        """Test registering an existing user"""
        with patch('streams.api.UserManagementService.register_user') as mock_register:
            mock_register.return_value = None
            
            response = self.client.post("/register", json={
                "username": "existing",
                "email": "existing@example.com",
                "password": "password123"
            })
            
            self.assertEqual(response.status_code, 400)
            
    def test_dashboard_authenticated(self):
        """Test dashboard access when authenticated"""
        stream = Stream.objects.create(user=self.user, title='Test Stream')
        
        # Mock authentication
        with patch.object(self.client, '_build_request') as mock_build:
            mock_request = Mock()
            mock_user = Mock()
            type(mock_user).is_authenticated = PropertyMock(return_value=True)
            mock_request.user = mock_user
            mock_build.return_value = mock_request
            
            with patch('streams.api.StreamManagementService.get_stream_for_user') as mock_get_stream:
                mock_get_stream.return_value = stream
                
                response = self.client.get("/dashboard")
                
                self.assertEqual(response.status_code, 200)
                
    def test_dashboard_unauthenticated(self):
        """Test dashboard access when not authenticated"""
        with patch.object(self.client, '_build_request') as mock_build:
            mock_request = Mock()
            mock_request.user.is_authenticated = False
            mock_build.return_value = mock_request
            
            response = self.client.get("/dashboard")
            
            self.assertEqual(response.status_code, 401)
            
    def test_list_recordings(self):
        """Test listing all recordings"""
        stream = Stream.objects.create(user=self.user, title='Test Stream')
        recording = Recording.objects.create(stream=stream, file_path='/path.mp4')
        
        with patch('streams.api.StreamManagementService.get_all_recordings') as mock_get_recordings:
            mock_get_recordings.return_value = [recording]
            
            response = self.client.get("/recordings")
            
            self.assertEqual(response.status_code, 200)
            mock_get_recordings.assert_called_once()
            
    def test_get_recording_exists(self):
        """Test getting a specific recording that exists"""
        stream = Stream.objects.create(user=self.user, title='Test Stream')
        recording = Recording.objects.create(stream=stream, file_path='/path.mp4')
        
        with patch('streams.api.StreamManagementService.get_recording_by_id') as mock_get_recording:
            mock_get_recording.return_value = recording
            
            response = self.client.get(f"/recordings/{recording.id}")
            
            self.assertEqual(response.status_code, 200)
            mock_get_recording.assert_called_once_with(recording.id)
            
    def test_get_recording_not_exists(self):
        """Test getting a recording that doesn't exist"""
        with patch('streams.api.StreamManagementService.get_recording_by_id') as mock_get_recording:
            mock_get_recording.return_value = None
            
            response = self.client.get("/recordings/999")
            
            self.assertEqual(response.status_code, 404)
            
    def test_list_live_streams(self):
        """Test listing live streams"""
        live_stream = Stream.objects.create(user=self.user, title='Live Stream', is_live=True)
        
        with patch('streams.api.StreamManagementService.get_live_streams') as mock_get_live:
            mock_get_live.return_value = [live_stream]
            
            response = self.client.get("/live-streams")
            
            self.assertEqual(response.status_code, 200)
            mock_get_live.assert_called_once()
