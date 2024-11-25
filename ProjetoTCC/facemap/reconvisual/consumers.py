import json
from channels.generic.websocket import AsyncWebsocketConsumer

class RecognitionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Conectar ao WebSocket
        await self.accept()

    async def disconnect(self, close_code):
        # Desconectar
        pass

    async def send_recognition_status(self, event):
        # Enviar a mensagem ao cliente WebSocket
        message = event['message']
        await self.send(text_data=json.dumps({
            'status': message
        }))