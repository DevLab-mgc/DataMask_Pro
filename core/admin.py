from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, FileUpload, ProcessingLog, PIIDetection

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'organization', 'is_staff', 'date_joined')
    search_fields = ('email', 'username', 'organization')
    ordering = ('-date_joined',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('organization', 'api_key')}),
    )

@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    list_display = ('original_filename', 'user', 'file_type', 'status', 'uploaded_at', 'processed_at')
    list_filter = ('status', 'file_type', 'uploaded_at')
    search_fields = ('original_filename', 'user__email')
    ordering = ('-uploaded_at',)

@admin.register(ProcessingLog)
class ProcessingLogAdmin(admin.ModelAdmin):
    list_display = ('file_upload', 'started_at', 'completed_at', 'success', 'processing_time')
    list_filter = ('success', 'started_at')
    search_fields = ('file_upload__original_filename', 'error_message')
    ordering = ('-started_at',)

@admin.register(PIIDetection)
class PIIDetectionAdmin(admin.ModelAdmin):
    list_display = ('file_upload', 'pii_type', 'line_number', 'confidence_score', 'detected_at')
    list_filter = ('pii_type', 'detected_at')
    search_fields = ('file_upload__original_filename', 'context')
    ordering = ('-detected_at',)
