import requests
import json
import urllib.parse
from typing import Dict, Optional

class RtmpServerApiClient:
    """
    A dedicated client for interacting with the external RTMP Server's management API.
    """
    def __init__(self, host: str, port: int):
        self.base_url = f"http://{host}:{port}/api2"   #checkout this URL format and it will be added from the .env file through service.py 
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'} 

    def _post(self, command: str, payload_data: Dict) -> requests.Response:
        """Helper to format and send the POST request."""
        full_payload = {command: payload_data}
        command_json_string = json.dumps(full_payload)
        data = urllib.parse.urlencode({'command': command_json_string})
        return requests.post(self.base_url, headers=self.headers, data=data)

    def add_stream(self, stream_name: str, disable_audio: bool = False) -> bool:
        """Adds a stream key to the RTMP server."""
        payload_data = {
            stream_name: {
                "source": "push://", 
                "disable_audio": disable_audio, 
            },
            "stop_sessions": True 
        }
        response = self._post("addstream", payload_data) 
        return response.status_code == 200 

    def delete_stream(self, stream_name: str) -> bool:
        """Deletes a stream key from the RTMP server."""
        payload_data = {
            stream_name: {
                "stop_sessions": True 
            }
        }
        response = self._post("deletestream", payload_data) 
        return response.status_code == 200 and "incomplete list" in response.text