from rest_framework import serializers
from .models import User, FileUpload, ProcessingLog, PIIDetection

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'organization', 'date_joined')
        read_only_fields = ('date_joined',)

class FileUploadSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = FileUpload
        fields = ('id', 'user', 'file', 'original_filename', 'file_type', 
                 'status', 'uploaded_at', 'processed_at')
        read_only_fields = ('status', 'uploaded_at', 'processed_at', 
                          'original_filename', 'file_type')

    def create(self, validated_data):
        # Set the original filename and file type
        file = validated_data['file']
        validated_data['original_filename'] = file.name
        validated_data['file_type'] = file.content_type
        return super().create(validated_data)

class ProcessingLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessingLog
        fields = ('id', 'file_upload', 'started_at', 'completed_at', 
                 'success', 'error_message', 'processing_time')
        read_only_fields = ('started_at', 'completed_at', 'processing_time')

class PIIDetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PIIDetection
        fields = ('id', 'file_upload', 'pii_type', 'line_number', 
                 'column_number', 'context', 'confidence_score', 
                 'masked_value', 'detected_at')
        read_only_fields = ('detected_at',)

class FileUploadDetailSerializer(FileUploadSerializer):
    """Detailed serializer for FileUpload including related data"""
    processing_logs = ProcessingLogSerializer(many=True, read_only=True)
    pii_detections = PIIDetectionSerializer(many=True, read_only=True)

    class Meta(FileUploadSerializer.Meta):
        fields = FileUploadSerializer.Meta.fields + ('processing_logs', 'pii_detections')
