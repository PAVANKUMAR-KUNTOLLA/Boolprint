import datetime
import uuid
from decouple import config
from django.db import models

def uuid_generator():
    return str(uuid.uuid4().hex)

class InventoryItem(models.Model):
    inventory_id = models.CharField(unique=True, max_length=255, default=uuid_generator)  #(chatroom_name)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name