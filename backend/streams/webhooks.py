import json, os , glob, time
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from .models import Stream, Recording

@csrf_exempt
def srs_on_publish_webhook(request: HttpRequest):
    print("--- ON_PUBLISH WEBHOOK RECEIVED ---")
    if request.method != 'POST':
        print("ERROR: Invalid request method.")
        return JsonResponse({'code': -1, 'message': 'Invalid method'}, status=405)

    try:
        data = json.loads(request.body)
        print(f"Webhook payload: {data}")
        stream_key = data.get('stream')

        if not stream_key:
            print("ERROR: Stream key not found in payload.")
            return JsonResponse({'code': -1, 'message': 'Stream key missing'}, status=400)

        print(f"Stream key from webhook is: {stream_key}")
        try:
            stream = Stream.objects.get(stream_key=stream_key)
            print(f"Found stream object in DB: {stream.user.username}")
            stream.is_live = True
            stream.hls_url = f"/live/{stream_key}.m3u8"
            stream.save()
            
            print(f"SUCCESS: Set is_live=True for user {stream.user.username}")
            return JsonResponse({'code': 0, 'message': 'Success'}, status=200)

        except Stream.DoesNotExist:
            print(f"ERROR: Stream.DoesNotExist for key: {stream_key}")
            return JsonResponse({'code': -1, 'message': 'Stream key not found'}, status=404)
    except json.JSONDecodeError:
        print("ERROR: Could not decode JSON from request body.")
        return JsonResponse({'code': -1, 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return JsonResponse({'code': -1, 'message': str(e)}, status=500)

@csrf_exempt
def srs_on_unpublish_webhook(request: HttpRequest):
    print("\n--- ON_UNPUBLISH WEBHOOK RECEIVED ---")
    if request.method != 'POST':
        return JsonResponse({'code': -1, 'message': 'Invalid method'}, status=405)

    try:
        data = json.loads(request.body)
        stream_key = data.get('stream')
        print(f"Unpublish for stream key: {stream_key}")

        if not stream_key:
            return JsonResponse({'code': -1, 'message': 'Stream key missing'}, status=400)

        stream = Stream.objects.get(stream_key=stream_key)
        stream.is_live = False
        stream.hls_url = None
        stream.save()
        print(f"Set is_live=False for user {stream.user.username}")

        recording_dir = "/media/record/live/"
        file_pattern = f'{recording_dir}{stream_key}_*.mp4'
        
        
        latest_file = None
        for i in range(5): 
            print(f"Attempt {i+1}: Searching for file with pattern: {file_pattern}")
            list_of_files = glob.glob(file_pattern)
            if list_of_files:
                print(f"Found {len(list_of_files)} matching files: {list_of_files}")
                latest_file = max(list_of_files, key=os.path.getctime)
                break 
            time.sleep(1) 
        
        if latest_file:
            filename = os.path.basename(latest_file)
            Recording.objects.create(
                stream=stream,
                file_path=f"/record/live/{filename}"
            )
            print(f"SUCCESS: Created Recording object for file: {filename}")
        else:
            print(f"ERROR: No recording files found after 5 attempts for pattern: {file_pattern}")

        return JsonResponse({'code': 0, 'message': 'Success'}, status=200)
        
    except Stream.DoesNotExist:
        print(f"ERROR: Stream.DoesNotExist in on_unpublish for key: {stream_key}")
        return JsonResponse({'code': -1, 'message': 'Stream key not found'}, status=404)
    except Exception as e:
        print(f"CRITICAL ERROR in on_unpublish webhook: {e}")
        return JsonResponse({'code': -1, 'message': str(e)}, status=500)