from django.contrib import admin
from .models import Guest

# Register your models here.
@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'status']
    search_fields = ['email', 'first_name', 'last_name']