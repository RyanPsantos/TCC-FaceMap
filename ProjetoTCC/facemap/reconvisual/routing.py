from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/recognition/", consumers.RecognitionConsumer.as_asgi()),
]