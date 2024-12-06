from django.contrib import admin
from .models import Request

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'pickup_location', 'dropoff_location', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('pickup_location', 'dropoff_location')
