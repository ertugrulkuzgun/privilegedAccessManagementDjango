from django.contrib import admin
from .models import AuthenticationType, Message, Room
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.
from .models import CustomizeUserModel

class UserInLine(admin.StackedInline):
    model = CustomizeUserModel
    can_delete = False
    verbose_name_plural = "customizeusermodel"

class UserAdmin(BaseUserAdmin):
    inlines = (UserInLine,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(AuthenticationType)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["user"]

    class Meta:
        model = Room

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["user","room","created_date"]

    class Meta:
        model = Message