from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Stream
from .serializers import  StreamKeySerializer

class StreamKeyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        stream, created = Stream.objects.get_or_create(user=request.user)
        serializer = StreamKeySerializer(stream)
        return Response(serializer.data)


class SrsOnPublishHookView(APIView):
    def post(self, request):
        stream_key = request.data.get('stream')
        try:
            stream = Stream.objects.get(stream_key=stream_key)
            stream.is_live = True
            stream.hls_url = f"/live/{stream_key}.m3u8"
            stream.save()
            return Response(status=status.HTTP_200_OK)
        except Stream.DoesNotExist:
          
            return Response(status=status.HTTP_404_NOT_FOUND)

class SrsOnUnpublishHookView(APIView):
    def post(self, request):
        stream_key = request.data.get('stream')
        try:
            stream = Stream.objects.get(stream_key=stream_key)
            stream.is_live = False
            stream.recorded_url = f"/record/live/" 
            stream.save()
            return Response(status=status.HTTP_200_OK)
        except Stream.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)