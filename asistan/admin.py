from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import InstagramAgents

@admin.register(InstagramAgents)
class InstagramAgentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'captions', 'is_active', 'date')
    list_filter = ('is_active', 'date')
    search_fields = ('captions', 'content', 'hashtag')
