# test_management_command.py
from django.test import TestCase
from django.core.management import call_command
from django.contrib.auth.models import User
from unittest.mock import patch, Mock, MagicMock
from io import StringIO
import json
from streams.models import Stream


class PollRtmpStreamsCommandTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.stream = Stream.objects.create(user=self.user, title='Test Stream')
        
    @patch('streams.management.commands.poll_rtmp_streams.time.sleep')
    @patch('streams.management.commands.poll_rtmp_streams.RtmpServerApiClient')
    def test_command_updates_live_status(self, mock_rtmp_client_class, mock_sleep):
        """Test that the command updates stream live status correctly"""
        # Mock the RTMP client
        mock_client = Mock()
        mock_rtmp_client_class.return_value = mock_client
        
        # Mock the API response with our stream as active
        mock_stats = {
            'streams': {
                self.stream.stream_key: {'status': 'live'}
            }
        }
        mock_client.get_stream_stats.return_value = mock_stats
        
        # Mock settings
        with patch('streams.management.commands.poll_rtmp_streams.settings') as mock_settings:
            mock_settings.RTMP_SERVER_HOST = 'localhost'
            mock_settings.RTMP_SERVER_API_PORT = 8080
            mock_settings.RTMP_HLS_BASE_URL = 'http://localhost:8080/hls/'
            mock_settings.RTMP_POLLING_INTERVAL = 1
            
            # Mock time.sleep to only run once
            def side_effect(interval):
                # After first sleep, raise KeyboardInterrupt to stop the loop
                raise KeyboardInterrupt()
            
            mock_sleep.side_effect = side_effect
            
            # Capture output
            out = StringIO()
            
            try:
                call_command('poll_rtmp_streams', stdout=out)
            except KeyboardInterrupt:
                pass  # Expected to exit this way
                
            # Refresh from database
            self.stream.refresh_from_db()
            
            # Check that stream was marked as live
            self.assertTrue(self.stream.is_live)
            self.assertEqual(self.stream.hls_url, f'http://localhost:8080/hls/{self.stream.stream_key}.m3u8')
            
    @patch('streams.management.commands.poll_rtmp_streams.time.sleep')
    @patch('streams.management.commands.poll_rtmp_streams.RtmpServerApiClient')
    def test_command_handles_api_failure(self, mock_rtmp_client_class, mock_sleep):
        """Test that the command handles API failures gracefully"""
        # Mock the RTMP client to return None (API failure)
        mock_client = Mock()
        mock_rtmp_client_class.return_value = mock_client
        mock_client.get_stream_stats.return_value = None
        
        def side_effect(interval):
            raise KeyboardInterrupt()
            
        mock_sleep.side_effect = side_effect
        
        with patch('streams.management.commands.poll_rtmp_streams.settings') as mock_settings:
            mock_settings.RTMP_SERVER_HOST = 'localhost'
            mock_settings.RTMP_SERVER_API_PORT = 8080
            mock_settings.RTMP_HLS_BASE_URL = 'http://localhost:8080/hls/'
            mock_settings.RTMP_POLLING_INTERVAL = 1
            
            out = StringIO()
            
            try:
                call_command('poll_rtmp_streams', stdout=out)
            except KeyboardInterrupt:
                pass
                
            output = out.getvalue()
            self.assertIn('No active streams reported', output)
