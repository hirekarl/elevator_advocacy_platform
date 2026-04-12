from django.contrib import admin
from .models import Building, ElevatorReport

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('bin', 'address', 'borough', 'created_at')
    search_fields = ('bin', 'address')

@admin.register(ElevatorReport)
class ElevatorReportAdmin(admin.ModelAdmin):
    list_display = ('building', 'status', 'user_id', 'reported_at', 'is_official')
    list_filter = ('status', 'is_official', 'reported_at')
    search_fields = ('building__bin', 'user_id')
