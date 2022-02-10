from django.contrib import admin
from .models import Post, PostUpdateEvent

# Register your models here.

admin.site.register(Post)
admin.site.register(PostUpdateEvent)
