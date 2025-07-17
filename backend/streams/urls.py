from django.urls import path
from .webhooks import srs_on_publish_webhook, srs_on_unpublish_webhook

urlpatterns = [
    path('srs/on_publish', srs_on_publish_webhook, name='webhook-on-publish'),
    path('srs/on_unpublish', srs_on_unpublish_webhook, name='webhook-on-unpublish'),
]