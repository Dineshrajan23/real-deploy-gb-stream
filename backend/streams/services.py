
from typing import Optional, List
from django.db import transaction, IntegrityError
from django.contrib.auth.models import User
from .models import Stream, Recording, generate_stream_key
from django.conf import settings
from .rtmp_api_service import RtmpServerApiClient




rtmp_api_client = RtmpServerApiClient(
    host=settings.RTMP_SERVER_HOST,
    port=settings.RTMP_SERVER_API_PORT
)


class StreamManagementService:
    """Handles all business logic related to stream management."""


    @staticmethod
    def get_stream_for_user(user: User) -> Stream:
        """SRP: Encapsulates the logic of getting or creating a stream for a user."""
        stream, created = Stream.objects.get_or_create(user=user)
        return stream

    @staticmethod
    def update_stream_title(user: User, new_title: str) -> Optional[Stream]:
        """SRP: Encapsulates the logic for updating a stream's title."""
        try:
            stream = Stream.objects.get(user=user)
            stream.title = new_title
            stream.save()
            return stream
        except Stream.DoesNotExist:
            return None

    @staticmethod
    def reset_stream_key(user: User) -> Optional[Stream]:
        """Proactively resets stream key and syncs with the RTMP server API."""
        try:
            stream = Stream.objects.get(user=user)
            old_stream_key = stream.stream_key
            new_stream_key = generate_stream_key()

            with transaction.atomic():
                stream.stream_key = new_stream_key
                stream.save()
            
            rtmp_api_client.delete_stream(old_stream_key)

            if not rtmp_api_client.add_stream(new_stream_key):
                print(f"ERROR: Failed to add new stream key {new_stream_key} to RTMP server.")

            
            return stream
        except Stream.DoesNotExist:
            return None

    @staticmethod
    def get_all_recordings() -> List[Recording]:
        """SRP: Encapsulates the query for listing all recordings."""
        return Recording.objects.select_related('stream__user').all().order_by('-created_at')

    @staticmethod
    def get_recording_by_id(recording_id: int) -> Optional[Recording]:
        """SRP: Encapsulates the query for getting a single recording."""
        return Recording.objects.select_related('stream__user').filter(pk=recording_id).first()

    @staticmethod
    def get_live_streams() -> List[Stream]:
        """SRP: Encapsulates the query for finding all live streams."""
        return Stream.objects.filter(is_live=True).select_related('user')


class UserManagementService:
    """Handles all business logic for user lifecycle management."""

    @staticmethod
    def register_user(username: str, email: str, password: str) -> Optional[User]:
        try:
            with transaction.atomic():
                if User.objects.filter(username=username).exists():
                    return None
                new_user = User.objects.create_user(username=username, email=email, password=password)
                Stream.objects.create(user=new_user)
            return new_user
        except IntegrityError as e:
            print(f"ERROR: IntegrityError during user registration: {e}")
            return None
        except Exception as e:
            print(f"ERROR: Exception during user registration: {e}")
            return None