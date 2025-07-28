import json
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from .services import StreamManagementService

@csrf_exempt
def srs_on_publish_webhook(request: HttpRequest):
    if request.method != 'POST':
        return JsonResponse({'code': -1, 'message': 'Invalid method'}, status=405)

    try:
        data = json.loads(request.body)
        stream_key = data.get('stream')
        if not stream_key:
            return JsonResponse({'code': -1, 'message': 'Stream key missing'}, status=400)

        stream = StreamManagementService.start_stream(stream_key)
        
        if stream:
            return JsonResponse({'code': 0, 'message': 'Success'}, status=200)
        else:
            return JsonResponse({'code': -1, 'message': 'Stream key not found'}, status=404)
            
    except Exception as e:
        print(f"CRITICAL ERROR in on_publish webhook: {e}")
        return JsonResponse({'code': -1, 'message': str(e)}, status=500)

@csrf_exempt
def srs_on_unpublish_webhook(request: HttpRequest):
    """
    REFACTORED: This view now only calls the stop_stream service method.
    It has a single, clear responsibility.
    """
    if request.method != 'POST':
        return JsonResponse({'code': -1, 'message': 'Invalid method'}, status=405)
    try:
        data = json.loads(request.body)
        stream_key = data.get('stream')
        if not stream_key:
            return JsonResponse({'code': -1, 'message': 'Stream key missing'}, status=400)

        stream = StreamManagementService.stop_stream(stream_key)

        if stream:
            return JsonResponse({'code': 0, 'message': 'Success'}, status=200)
        else:
            return JsonResponse({'code': -1, 'message': 'Stream key not found'}, status=404)
    except Exception as e:
        print(f"CRITICAL ERROR in on_unpublish webhook: {e}")
        return JsonResponse({'code': -1, 'message': str(e)}, status=500)

@csrf_exempt
def srs_on_dvr_webhook(request: HttpRequest):
    """
    NEW: This view handles the on_dvr event, which is the correct
    place to manage completed recordings.
    """
    if request.method != 'POST':
        return JsonResponse({'code': -1, 'message': 'Invalid method'}, status=405)
    try:
        data = json.loads(request.body)
        stream_key = data.get('stream')
        file_path = data.get('file') 

        if not stream_key or not file_path:
            return JsonResponse({'code': -1, 'message': 'Payload missing stream or file'}, status=400)

        recording = StreamManagementService.create_recording(stream_key, file_path)

        if recording:
            return JsonResponse({'code': 0, 'message': 'Recording saved'}, status=200)
        else:
            return JsonResponse({'code': -1, 'message': 'Failed to create recording'}, status=404)
    except Exception as e:
        print(f"CRITICAL ERROR in on_dvr webhook: {e}")
        return JsonResponse({'code': -1, 'message': str(e)}, status=500)