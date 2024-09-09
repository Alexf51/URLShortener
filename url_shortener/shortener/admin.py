from django.contrib import admin
from .models import URL

class URLAdmin(admin.ModelAdmin):
    list_display = ('original_url', 'short_url', 'clicks', 'created_at', 'user')
    list_filter = ('created_at', 'user')
    search_fields = ('original_url', 'short_url')
    ordering = ('-created_at',)

admin.site.register(URL, URLAdmin)