from ninja import NinjaAPI
from django.http import HttpRequest
from typing import List
from .schemas import (
    StreamKeySchema, RecordingSchema, StreamUpdateSchema, LoginSchema, 
    DashboardSchema, LiveStreamSchema, UserRegistrationSchema
)
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login, logout
from .services import StreamManagementService, UserManagementService

api = NinjaAPI(csrf=True, urls_namespace='streams')

@api.get("/csrf-cookie")
def get_csrf_cookie(request: HttpRequest):
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

@api.post("/register")
def register_user(request, payload: UserRegistrationSchema):
    new_user = UserManagementService.register_user(
        username=payload.username,
        email=payload.email,
        password=payload.password
    )
    if new_user:
        return 201, {"success": True, "username": new_user.username}
    else:
        return 400, {"detail": "Username already taken."}

@api.get("/dashboard", response=DashboardSchema)
def get_dashboard_info(request: HttpRequest):
    if not request.user.is_authenticated:
        return 401, {"detail": "Authentication required"}
    stream = StreamManagementService.get_stream_for_user(request.user)
    return stream 

@api.patch("/dashboard", response=DashboardSchema)
def update_stream_info(request: HttpRequest, payload: StreamUpdateSchema):
    if not request.user.is_authenticated:
        return 401, {"detail": "Authentication required"}
    stream = StreamManagementService.update_stream_title(request.user, payload.title)
    if stream:
        return stream
    return 404, {"detail": "Stream not found for user."}

@api.post("/dashboard/reset-key", response=StreamKeySchema)
def reset_stream_key(request: HttpRequest):
    if not request.user.is_authenticated:
        return 401, {"detail": "Authentication required."}
    stream = StreamManagementService.reset_stream_key(request.user)
    if stream:
        return stream
    return 404, {"detail": "Stream not found for user."}
  
@api.get("/recordings", response=List[RecordingSchema])
def list_recordings(request: HttpRequest):
    recordings = StreamManagementService.get_all_recordings()
    return recordings

@api.get("/recordings/{recording_id}", response=RecordingSchema)
def get_recording(request: HttpRequest, recording_id: int):
    recording = StreamManagementService.get_recording_by_id(recording_id)
    if recording:
        return recording
    return 404, {"message": "Recording not found"}

@api.get("/live-streams", response=List[LiveStreamSchema])
def list_live_streams(request: HttpRequest):
    live_streams = StreamManagementService.get_live_streams()
    return live_streams