from ninja import NinjaAPI
from django.http import HttpRequest
from .models import Stream, generate_stream_key, Recording
from typing import List
from .schemas import StreamKeySchema,  RecordingSchema,  StreamUpdateSchema, LoginSchema, DashboardSchema, LiveStreamSchema, UserRegistrationSchema
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


api = NinjaAPI(csrf=True, urls_namespace='streams')


@api.get("/csrf-cookie")
def get_csrf_cookie(request: HttpRequest):
    """
    Returns a CSRF cookie to the client.
    """
    get_token(request)
    return {"detail": "CSRF cookie set"}

@api.post("/login")
def user_login(request: HttpRequest, payload: LoginSchema):
    user = authenticate(username=payload.username, password=payload.password)
    if user is not None:
        login(request, user)
        return {"success": True, "username": user.username}
    return 401, {"success": False, "detail": "Invalid credentials"}

@api.post("/logout")
def user_logout(request: HttpRequest):
    logout(request)
    return {"success": True}



@api.get("/dashboard", response=DashboardSchema)
def get_dashboard_info(request: HttpRequest):
    if not request.user.is_authenticated:
        return 401, {"detail": "Authentication required."}
    
    stream, created = Stream.objects.get_or_create(user=request.user)
    return {
        "stream_key": stream.stream_key,
        "stream_title": stream.title,
        "is_live": stream.is_live,
    }

@api.patch("/dashboard", response=DashboardSchema)
def update_stream_info(request: HttpRequest, payload: StreamUpdateSchema):
    if not request.user.is_authenticated:
        return 401, {"detail": "Authentication required."}
    
    stream = Stream.objects.get(user=request.user)
    stream.title = payload.title
    stream.save()
    return stream

@api.post("/dashboard/reset-key", response=StreamKeySchema)
def reset_stream_key(request: HttpRequest):
    if not request.user.is_authenticated:
        return 401, {"detail": "Authentication required."}
    
    stream = Stream.objects.get(user=request.user)
    stream.stream_key = generate_stream_key() # Generate a new key
    stream.save()
    return stream

@api.get("/key", response=StreamKeySchema)
def get_stream_key(request: HttpRequest):
    """
    Returns the stream key for the authenticated user.
    Creates a stream record if one doesn't exist.
    """
    if not request.user.is_authenticated:
   
        return 401, {"detail": "Authentication required."}


    stream, created = Stream.objects.get_or_create(user=request.user)

    return stream

@api.get("/recordings", response=List[RecordingSchema])
def list_recordings(request: HttpRequest):
    """
    Returns a list of all saved recording sessions.
    """
    recordings = Recording.objects.select_related('stream__user').all().order_by('-created_at')
    return recordings


@api.get("/recordings/{recording_id}", response=RecordingSchema)
def get_recording(request: HttpRequest, recording_id: int):
    try:
        recording = Recording.objects.select_related('stream__user').get(pk=recording_id)
        return recording
    except Recording.DoesNotExist:
        return 404, {"message": "Recording not found"}
    

@api.get("/live-streams", response=List[LiveStreamSchema])
def list_live_streams(request: HttpRequest):
    """
    Returns a list of all streams that are currently live.
    """
    live_streams = Stream.objects.filter(is_live=True).select_related('user')
    return live_streams

@api.post("/register")
def register_user(request, payload: UserRegistrationSchema):
    """
    Registers a new user with the provided username, email, and password.
    """
    if User.objects.filter(username=payload.username).exists():
        return 400, {"detail": "Username already taken."}
    
    new_user = User.objects.create_user(
        username=payload.username,
        email=payload.email,
        password=payload.password
    )
    
    Stream.objects.create(user=new_user)
    
    return {"detail": "User registered successfully", "username": new_user.username}

