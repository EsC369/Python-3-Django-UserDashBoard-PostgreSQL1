from django.contrib import admin
from apps.UserDB_app.models import User, Message, Comment

admin.site.register(User)
admin.site.register(Message)
admin.site.register(Comment)