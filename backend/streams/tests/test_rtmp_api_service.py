from django.test import TestCase
from unittest.mock import Mock, patch
import json
from streams.rtmp_api_service import RtmpServerApiClient


class RtmpServerApiClientTest(TestCase):
    def setUp(self):
        self.client = RtmpServerApiClient(host='localhost', port=8080)
        
    def test_init(self):
        """Test initialization of RtmpServerApiClient"""
        self.assertEqual(self.client.base_url, 'http://localhost:8080/api2')
        self.assertEqual(self.client.headers, {'Content-Type': 'application/x-www-form-urlencoded'})
        
    @patch('streams.rtmp_api_service.requests.post')
    def test_post_method(self, mock_post):
        """Test the _post helper method"""
        mock_response = Mock()
        mock_post.return_value = mock_response
        
        payload = {"test": "data"}
        response = self.client._post("testcommand", payload)
        
        # Verify the request was made
        mock_post.assert_called_once()
        self.assertEqual(response, mock_response)
        
    @patch('streams.rtmp_api_service.requests.post')
    def test_add_stream_success(self, mock_post):
        """Test successful stream addition"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        result = self.client.add_stream('test_stream')
        
        self.assertTrue(result)
        mock_post.assert_called_once()
        
    @patch('streams.rtmp_api_service.requests.post')
    def test_add_stream_failure(self, mock_post):
        """Test failed stream addition"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response
        
        result = self.client.add_stream('test_stream')
        
        self.assertFalse(result)
        
    @patch('streams.rtmp_api_service.requests.post')
    def test_delete_stream_success(self, mock_post):
        """Test successful stream deletion"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "some response with incomplete list"
        mock_post.return_value = mock_response
        
        result = self.client.delete_stream('test_stream')
        
        self.assertTrue(result)
        
    @patch('streams.rtmp_api_service.requests.post')
    def test_delete_stream_failure(self, mock_post):
        """Test failed stream deletion"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "response without expected text"
        mock_post.return_value = mock_response
        
        result = self.client.delete_stream('test_stream')
        
        self.assertFalse(result)