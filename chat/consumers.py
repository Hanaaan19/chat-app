import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils import timezone
from .models import Message, CustomUser


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.user = self.scope["user"]

    
        if self.user.is_anonymous:
            self.close()
            return

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group = f"chat_{self.room_name}"
        self.user_group = f"user_{self.user.id}"
        self.online_group = "online_users"

        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group,
            self.channel_name
        )

        
        async_to_sync(self.channel_layer.group_add)(
            self.user_group,
            self.channel_name
        )

        
        async_to_sync(self.channel_layer.group_add)(
            self.online_group,
            self.channel_name
        )

        
        self.user.is_online = True
        self.user.last_seen = timezone.now()
        self.user.save()

        
        async_to_sync(self.channel_layer.group_send)(
            self.online_group,
            {
                "type": "user_status",
                "user_id": self.user.id,
                "is_online": True,
                "last_seen": self.user.last_seen.isoformat(),
            }
        )

        self.accept()

    def disconnect(self, close_code):

        
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group,
            self.channel_name
        )

        async_to_sync(self.channel_layer.group_discard)(
            self.user_group,
            self.channel_name
        )

        async_to_sync(self.channel_layer.group_discard)(
            self.online_group,
            self.channel_name
        )

        
        self.user.is_online = False
        self.user.last_seen = timezone.now()
        self.user.save()

        async_to_sync(self.channel_layer.group_send)(
            self.online_group,
            {
                "type": "user_status",
                "user_id": self.user.id,
                "is_online": False,
                "last_seen": self.user.last_seen.isoformat(),
            }
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")

        if action == "message":
            message = data.get("message", "").strip()
            receiver_id = data.get("receiver_id")

            if not message:
                return

            try:
                receiver = CustomUser.objects.get(id=receiver_id)
            except CustomUser.DoesNotExist:
                return

            msg = Message.objects.create(
                sender=self.user,
                receiver=receiver,
                content=message
            )

            async_to_sync(self.channel_layer.group_send)(
                self.room_group,
                {
                    "type": "chat_message",
                    "message": msg.content,
                    "sender_id": self.user.id,
                    "message_id": msg.id,
                }
            )

            
            async_to_sync(self.channel_layer.group_send)(
                f"user_{receiver.id}",
                {
                    "type": "unread_update",
                    "sender_id": self.user.id,
                }
            )

        
        elif action == "typing_start":
            async_to_sync(self.channel_layer.group_send)(
                self.room_group,
                {
                    "type": "typing_status",
                    "sender_id": self.user.id,
                    "is_typing": True,
                }
            )

        
        elif action == "typing_stop":
            async_to_sync(self.channel_layer.group_send)(
                self.room_group,
                {
                    "type": "typing_status",
                    "sender_id": self.user.id,
                    "is_typing": False,
                }
            )

        
        elif action == "read":
            ids = data.get("message_ids", [])

            if ids:
                Message.objects.filter(id__in=ids).update(is_read=True)

                async_to_sync(self.channel_layer.group_send)(
                    self.room_group,
                    {
                        "type": "read_status",
                        "message_ids": ids,
                    }
                )

        
        elif action == "delete":
            message_id = data.get("message_id")

            Message.objects.filter(
                id=message_id,
                sender=self.user
            ).delete()

            async_to_sync(self.channel_layer.group_send)(
                self.room_group,
                {
                    "type": "delete_message",
                    "message_id": message_id,
                }
            )

    

    def chat_message(self, event):
        self.send(text_data=json.dumps({
            "type": "message",
            "message": event["message"],
            "sender_id": event["sender_id"],
            "message_id": event["message_id"],
        }))

    def typing_status(self, event):
        self.send(text_data=json.dumps({
            "type": "typing",
            "sender_id": event["sender_id"],
            "is_typing": event["is_typing"],
        }))

    def read_status(self, event):
        self.send(text_data=json.dumps({
            "type": "read",
            "message_ids": event["message_ids"],
        }))

    def unread_update(self, event):
        sender_id = event["sender_id"]

        count = Message.objects.filter(
            sender_id=sender_id,
            receiver=self.user,
            is_read=False
        ).count()

        self.send(text_data=json.dumps({
            "type": "unread_update",
            "sender_id": sender_id,
            "unread_count": count,
        }))

    def delete_message(self, event):
        self.send(text_data=json.dumps({
            "type": "delete",
            "message_id": event["message_id"],
        }))

    def user_status(self, event):
        self.send(text_data=json.dumps({
            "type": "user_status",
            "user_id": event["user_id"],
            "is_online": event["is_online"],
            "last_seen": event.get("last_seen"),
        }))

    def new_user_event(self, event):
        self.send(text_data=json.dumps({
            "type": "new_user",
            "user_id": event["user_id"],
            "username": event["username"],
        }))    