import os
from typing import Optional, List
from django.db import transaction, IntegrityError
from django.contrib.auth.models import User
from .models import Stream, Recording, generate_stream_key
from django.conf import settings

# Default SRS web root prefix for recordings
SRS_WEB_ROOT_PREFIX_DEFAULT = "/usr/local/srs/objs/nginx/html"

class StreamManagementService:
    """Handles all business logic for streams and recordings."""

    @staticmethod
    def start_stream(stream_key: str) -> Optional[Stream]:
        try:
            with transaction.atomic():
                stream = Stream.objects.select_for_update().get(stream_key=stream_key)
                stream.is_live = True
                stream.hls_url = f"/live/{stream_key}.m3u8"
                stream.save()
                print(f"SUCCESS: Stream started for user {stream.user.username}")
                return stream
        except Stream.DoesNotExist:
            print(f"ERROR: Stream.DoesNotExist on start for key: {stream_key}")
            return None

    @staticmethod
    def stop_stream(stream_key: str) -> Optional[Stream]:
        try:
            with transaction.atomic():
                stream = Stream.objects.select_for_update().get(stream_key=stream_key)
                stream.is_live = False
                stream.hls_url = None
                stream.save()
                print(f"SUCCESS: Stream stopped for user {stream.user.username}")
                return stream
        except Stream.DoesNotExist:
            print(f"ERROR: Stream.DoesNotExist on stop for key: {stream_key}")
            return None

    @staticmethod
    def create_recording(stream_key: str, file_path_from_srs: str) -> Optional[Recording]:
        """
        Creates a Recording entry from the on_dvr webhook payload.
        This is deterministic and removes the need for filesystem polling.
        Validates that the file path exists and is accessible before creating the record.
        """
        try:
            stream = Stream.objects.get(stream_key=stream_key)
            web_root_prefix = getattr(
                   settings, 
                   'SRS_WEB_ROOT_PREFIX_DEFAULT', 
                   SRS_WEB_ROOT_PREFIX_DEFAULT
                )
            if file_path_from_srs.startswith(web_root_prefix):
                public_url_path = file_path_from_srs[len(web_root_prefix):]
            else:
                public_url_path = file_path_from_srs

            # Validate file existence and accessibility
            if not os.path.exists(file_path_from_srs) or not os.access(file_path_from_srs, os.R_OK):
                print(f"ERROR: File does not exist or is not accessible: {file_path_from_srs}")
                return None

            recording = Recording.objects.create(
                stream=stream,
                file_path=public_url_path
            )
            print(f"SUCCESS: Created Recording object for file: {public_url_path}")
            return recording
        except Stream.DoesNotExist:
            print(f"ERROR: Stream.DoesNotExist on recording creation for key: {stream_key}")
            return None
            return None


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
        """SRP: Encapsulates the logic for generating and saving a new stream key."""
        try:
            stream = Stream.objects.get(user=user)
            stream.stream_key = generate_stream_key()
            stream.save()
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