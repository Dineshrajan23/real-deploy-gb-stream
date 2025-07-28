from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .models import Stream
from .serializers import StreamKeySerializer

from .services import StreamManagementService, UserManagementService

class StreamKeyView(APIView):
    """Provides the stream key for the authenticated user."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        stream, created = Stream.objects.get_or_create(user=request.user)
        serializer = StreamKeySerializer(stream)
        return Response(serializer.data)

# --- SRS Webhook Views ---

class SrsOnPublishHookView(APIView):
    """Handles the on_publish event from SRS."""
    permission_classes = [AllowAny] # Webhooks must be publicly accessible

    def post(self, request):
        stream_key = request.data.get('stream')
        if not stream_key:
            return Response(
                {"detail": "Stream key missing from payload."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        stream = StreamManagementService.start_stream(stream_key)
        
        if stream:
            return Response({"code": 0, "message": "Success"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"code": -1, "message": "Stream key not found."},
                status=status.HTTP_404_NOT_FOUND
            )

class SrsOnUnpublishHookView(APIView):
    """Handles the on_unpublish event from SRS."""
    permission_classes = [AllowAny]

    def post(self, request):
        stream_key = request.data.get('stream')
        if not stream_key:
            return Response(
                {"detail": "Stream key missing from payload."},
                status=status.HTTP_400_BAD_REQUEST
            )

        stream = StreamManagementService.stop_stream(stream_key)
        
        if stream:
            return Response({"code": 0, "message": "Success"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"code": -1, "message": "Stream key not found."},
                status=status.HTTP_404_NOT_FOUND
            )

class SrsOnDvrHookView(APIView):
    """
    Handles the on_dvr event, which fires when a recording is complete.
    This is the new, reliable way to save recordings.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        stream_key = request.data.get('stream')
        file_path = request.data.get('file') # SRS provides the file path

        if not stream_key or not file_path:
            return Response(
                {"detail": "Payload missing 'stream' or 'file' key."},
                status=status.HTTP_400_BAD_REQUEST
            )

        recording = StreamManagementService.create_recording(stream_key, file_path)

        if recording:
            return Response({"code": 0, "message": "Recording saved"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"code": -1, "message": "Failed to create recording. Stream key may not exist."},
                status=status.HTTP_404_NOT_FOUND
            )