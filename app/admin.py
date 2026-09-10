from django.contrib import admin
from .models import Reporter, Desk, News


@admin.register(Reporter)
class ReporterAdmin(admin.ModelAdmin):
    list_display = ('reporter_id', 'name', 'phone_number', 'district', 'is_active', 'created_at')
    list_filter = ('district', 'is_active', 'created_at')
    search_fields = ('reporter_id', 'name', 'phone_number', 'district', 'address')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Desk)
class DeskAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'phone_number', 'email')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('headline', 'news_type', 'category', 'district', 'reporter', 'status', 'created_at')
    list_filter = ('news_type', 'category', 'district', 'status', 'created_at')
    search_fields = ('headline', 'description', 'location', 'district', 'byte_interview')
    readonly_fields = ('created_at', 'updated_at')
