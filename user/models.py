from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
import uuid

# Create your models here.

class AuthenticationType(models.Model):
    authenticationName = models.CharField(max_length=100)
    ls = models.BooleanField()
    cd = models.BooleanField()
    

    def __str__(self):
        return self.authenticationName

class CustomizeUserModel(models.Model):
    class Choices(models.IntegerChoices):
        FULL_AUTHORIZED = 1
        VASIFSIZ = 2 
        ORTA_VASIFSIZ = 3
        ORTA_VASIFLI = 4

    customizedUser = models.OneToOneField(User, on_delete=models.CASCADE)
    authType = models.IntegerField(choices=Choices.choices)
    
class Room(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    user = models.ForeignKey(User,related_name="room_first",on_delete=models.CASCADE)

class Message(models.Model):
    user = models.ForeignKey(User,related_name="messages",verbose_name="Kullanıcı",on_delete=models.CASCADE)
    room = models.ForeignKey(Room,related_name="messages",verbose_name="Oda",on_delete=models.CASCADE)
    content = models.TextField(verbose_name="Message content")
    created_date = models.DateTimeField(auto_now_add=True)

