from django.contrib import admin

from django.contrib import admin
from .models import SpeechCard

@admin.register(SpeechCard)
class SpeechCardAdmin(admin.ModelAdmin):
    list_display = ('text', 'user')
    search_fields = ('text', 'user__username')
    list_filter = ('user',)

