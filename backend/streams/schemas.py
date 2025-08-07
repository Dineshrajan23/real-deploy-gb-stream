from ninja import Schema
from typing import Optional, List
from datetime import datetime
from pydantic import Field

class UserSchema(Schema):
    username: str
    email : str

class StreamKeySchema(Schema):
    stream_key: str

class StreamOutSchema(Schema):
    title: Optional[str] = None
    is_live: bool
    hls_url: Optional[str] = None
    recorded_url: Optional[str] = None

class SrsWebhookSchema(Schema):
    action: str
    client_id: str
    ip: str
    vhost: str
    app: str
    stream: str 

class LoginSchema(Schema):
    username: str
    password: str

class DashboardSchema(Schema):
    stream_key: str
    stream_title: Optional[str] = None
    is_live: bool

class StreamUpdateSchema(Schema):
    title: str

class UserRegistrationSchema(Schema):
    username: str
    email: str
    password: str

class StreamInfoSchema(Schema):
    title: Optional[str]
    user: UserSchema

class RecordingSchema(Schema):
    id: int
    file_path: str
    created_at: datetime
    stream: StreamInfoSchema 

class LiveStreamSchema(Schema):
    id: int
    title: Optional[str]
    hls_url: str
    user: UserSchema

class DashboardUpdateSchema(Schema):
    title: str 