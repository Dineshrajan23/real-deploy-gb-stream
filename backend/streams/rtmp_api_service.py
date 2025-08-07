# backend/streams/rtmp_integration/rtmp_api_client.py

import requests
import json
import urllib.parse
from typing import Dict, Optional, List, Any

class RtmpServerApiClient:
    """
    A dedicated client for interacting with the external RTMP Server's management API.
    """
    def __init__(self, host: str, api_port: int):
        self.base_url = f"http://{host}:{api_port}/api2"
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    def _post(self, command_name: str, payload_data: Dict) -> Optional[Dict]:
        """
        Helper to format and send the POST request to the MistServer API.
        Returns the JSON response or None on failure.
        """
        full_payload = {command_name: payload_data}
        command_json_string = json.dumps(full_payload)
        data = urllib.parse.urlencode({'command': command_json_string})

        try:
            response = requests.post(self.base_url, headers=self.headers, data=data)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            
            # --- DEBUG LOGGING START ---
            print(f"DEBUG: API call to {self.base_url} with command '{command_name}' successful.")
            print(f"DEBUG: Raw response text: {response.text}")
            # --- DEBUG LOGGING END ---

            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Error during API call to {self.base_url} with command '{command_name}': {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"ERROR: Response status: {e.response.status_code}")
                print(f"ERROR: Response body: {e.response.text}")
            return None
        except json.JSONDecodeError as e:
            print(f"ERROR: Error decoding JSON response for command '{command_name}': {e}. Response text: {response.text}")
            return None

    def add_stream(self, stream_name: str, disable_audio: bool = False) -> bool:
        """
        Adds a stream key to the RTMP server.
        Returns True on success, False otherwise.
        """
        payload_data = {
            stream_name: {
                "source": "push://",
                "disable_audio": disable_audio,
            },
            "stop_sessions": True
        }
        response_data = self._post("addstream", payload_data)
        
        if response_data and isinstance(response_data, dict):
            if stream_name in response_data and isinstance(response_data[stream_name], dict):
                print(f"DEBUG: add_stream for '{stream_name}' successful (key with empty dict).")
                return True
            if response_data.get('success') is True:
                print(f"DEBUG: add_stream for '{stream_name}' successful (general 'success' flag).")
                return True
            stream_result = response_data.get(stream_name)
            if stream_result and isinstance(stream_result, dict) and stream_result.get('status') == 'OK':
                print(f"DEBUG: add_stream for '{stream_name}' successful (status 'OK').")
                return True
        
        print(f"ERROR: Failed to add stream '{stream_name}' to RTMP server. Response: {response_data}")
        return False

    def delete_stream(self, stream_name: str) -> bool:
        """
        Deletes a stream key from the RTMP server.
        Returns True on success, False otherwise.
        """
        payload_data = {
            stream_name: {
                "stop_sessions": True
            }
        }
        response_data = self._post("deletestream", payload_data)
        return response_data is not None and "incomplete list" not in str(response_data)


    def get_stream_stats(self) -> List[Dict[str, Any]]:
        """
        Gets realtime statistics of all running streams from the RTMP server.
        Returns a list of dictionaries, where each dictionary represents a stream's data.
        """
        payload_data = {"streams_status": True}
        response_data = self._post("streams_status", payload_data) 

        # --- CRITICAL FIX START ---
        # MistServer's 'streams_status' command returns data nested under 'streams_status' key.
        # The value of 'streams_status' is a dictionary where keys are stream names.
        if response_data and isinstance(response_data, dict) and 'streams_status' in response_data:
            streams_data = response_data['streams_status'] # Access the correct nested dictionary
            formatted_streams = []
            for stream_name, details in streams_data.items():
                # Add stream_name to the details for easier access in the poller
                details['stream_name'] = stream_name
                formatted_streams.append(details)
            return formatted_streams
        # --- CRITICAL FIX END ---
        elif response_data:
            # If 'streams_status' key is missing but response_data is not None, it might mean no streams are live
            return []
        else:
            # If response_data is None, an error occurred during the POST request
            return []

