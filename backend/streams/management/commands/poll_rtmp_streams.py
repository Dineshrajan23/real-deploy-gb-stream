import time
import json 
import requests 
from django.core.management.base import BaseCommand
from django.conf import settings
from streams.models import Stream
# Ensure this import path is correct for your project structure
from streams.rtmp_api_service import RtmpServerApiClient 

class Command(BaseCommand):
    help = 'Polls the external RTMP server for live stream status and updates database.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting RTMP stream polling..."))
        rtmp_api_client = RtmpServerApiClient(
            host=settings.RTMP_SERVER_HOST,
            api_port=settings.RTMP_SERVER_API_PORT 
        )

        RTMP_HLS_BASE_URL = settings.RTMP_HLS_BASE_URL
        
        # Use the correct setting name: RTMP_POLLING_INTERVAL_SECONDS
        polling_interval = getattr(settings, 'RTMP_POLLING_INTERVAL_SECONDS', 15) # Default to 15 seconds if not set


        while True:
            try:
                # Fetch live stream statistics from MistServer
                stats_response = rtmp_api_client.get_stream_stats()
                
                active_stream_names = set()
                # MistServer's get_stream_stats returns a list of dictionaries, not a single dict with a 'streams' key.
                # The rtmp_api_client.get_stream_stats method was updated to return a list of dicts.
                if stats_response and isinstance(stats_response, list):
                    # Extract stream_name from each dictionary in the list
                    active_stream_names = {s.get('stream_name') for s in stats_response if 'stream_name' in s}
                    self.stdout.write(f"Active streams reported by RTMP server: {active_stream_names}")
                elif stats_response is not None:
                    # This branch means get_stream_stats returned something, but not a list as expected.
                    # It might be the raw JSON response if _post didn't extract 'streams' correctly.
                    # Let's try to parse it if it contains 'streams_status'
                    if isinstance(stats_response, dict) and 'streams_status' in stats_response:
                        # Correctly access the nested 'streams_status' dictionary
                        nested_streams = stats_response['streams_status']
                        active_stream_names = set(nested_streams.keys())
                        self.stdout.write(f"Active streams reported by RTMP server (parsed from nested): {active_stream_names}")
                    else:
                        self.stdout.write(self.style.WARNING(f"RTMP server returned unexpected stats format: {stats_response}"))
                else:
                    self.stdout.write("No active streams reported by RTMP server or API call failed.")



                all_streams = Stream.objects.all()
                
                for stream in all_streams:
                    is_currently_live = stream.stream_key in active_stream_names
                    
                    if stream.is_live != is_currently_live:
                        stream.is_live = is_currently_live
                        if is_currently_live:
                            stream.hls_url = f"{RTMP_HLS_BASE_URL}{stream.stream_key}/playlist.m3u8"
                        else:
                            stream.hls_url = None 
                        stream.save()
                        self.stdout.write(self.style.SUCCESS(
                            f"Updated stream '{stream.user.username}' (key: {stream.stream_key}) to is_live={is_currently_live}"
                        ))
                    elif is_currently_live and not stream.hls_url:
                        # This handles cases where a stream becomes live, but its HLS URL wasn't set for some reason
                        stream.hls_url = f"{RTMP_HLS_BASE_URL}{stream.stream_key}/playlist.m3u8"
                        stream.save()
                        self.stdout.write(self.style.SUCCESS(
                            f"Set HLS URL for live stream '{stream.user.username}' (key: {stream.stream_key})"
                        ))

            except requests.exceptions.ConnectionError as ce:
                self.stderr.write(self.style.ERROR(f"Connection error to RTMP server API: {ce}"))
            except json.JSONDecodeError as jde:
                self.stderr.write(self.style.ERROR(f"JSON decode error from RTMP server API response: {jde}"))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"An unexpected error occurred during RTMP stream polling: {e}"))


            time.sleep(polling_interval)

        self.stdout.write(self.style.SUCCESS("RTMP stream polling stopped."))

