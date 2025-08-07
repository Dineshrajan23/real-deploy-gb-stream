import uuid
from django.db import models
from django.contrib.auth.models import User

def generate_stream_key() -> str:
    return  "default.stream"

class Stream(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stream'  )
    title = models.CharField(max_length = 200, blank = False, null = False)
    stream_key = models.CharField(max_length= 32, default= generate_stream_key, unique= True)
    is_live = models.BooleanField(default=False)
    hls_url = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

class Recording(models.Model):
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE, related_name='recordings')
    file_path = models.CharField(max_length=255) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recording for {self.stream.user.username} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"