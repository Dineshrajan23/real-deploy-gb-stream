import time
import json 
import requests 
from django.core.management.base import BaseCommand
from django.conf import settings
from streams.models import Stream
from streams.rtmp_api_service import RtmpServerApiClient

class Command(BaseCommand):
    help = 'Polls the external RTMP server for live stream status and updates database.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting RTMP stream polling..."))
        rtmp_api_client = RtmpServerApiClient(
            host=getattr(settings, 'RTMP_SERVER_HOST', 'aanis-server-ip'),
            port=getattr(settings, 'RTMP_SERVER_API_PORT', 8080)
        )

        RTMP_HLS_BASE_URL = getattr(settings, 'RTMP_HLS_BASE_URL', 'http://aanis-server-ip:8080/live/')

        polling_interval = getattr(settings, 'RTMP_POLLING_INTERVAL_SECONDS', 15) 

        while True:
            try:
    
                stats = rtmp_api_client.get_stream_stats()
                
                active_stream_names = set()
                if stats and isinstance(stats, dict) and 'streams' in stats:
       
                    active_stream_names = set(stats['streams'].keys()) 
                    self.stdout.write(f"Active streams reported by RTMP server: {active_stream_names}")
                elif stats is not None:
    
                    self.stdout.write(self.style.WARNING(f"RTMP server returned unexpected stats format: {stats}"))
                else:
                    self.stdout.write("No active streams reported by RTMP server or API call failed.")


                all_streams = Stream.objects.all()
                
                for stream in all_streams:
     
                    is_currently_live = stream.stream_key in active_stream_names
                    
      
                    if stream.is_live != is_currently_live:
                        stream.is_live = is_currently_live
                        if is_currently_live:
          
                            stream.hls_url = f"{RTMP_HLS_BASE_URL}{stream.stream_key}.m3u8"
                        else:
                            stream.hls_url = None 
                        stream.save()
                        self.stdout.write(self.style.SUCCESS(
                            f"Updated stream '{stream.user.username}' (key: {stream.stream_key}) to is_live={is_currently_live}"
                        ))
                    elif is_currently_live and not stream.hls_url:
      
                        stream.hls_url = f"{RTMP_HLS_BASE_URL}{stream.stream_key}.m3u8"
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

