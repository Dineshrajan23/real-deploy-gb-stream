from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Stream
from .serializers import StreamKeySerializer


class StreamKeyView(APIView):
    """Provides the stream key for the authenticated user."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        stream, created = Stream.objects.get_or_create(user=request.user)
        serializer = StreamKeySerializer(stream)
        return Response(serializer.data)
