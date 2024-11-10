from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
import google.generativeai as genai
from django.conf import settings
from .models import User, FileUpload, ProcessingLog, PIIDetection
from .serializers import (
    UserSerializer, 
    FileUploadSerializer, 
    FileUploadDetailSerializer,
    ProcessingLogSerializer, 
    PIIDetectionSerializer
)

# Configure Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only see their own profile
        if not self.request.user.is_staff:
            return User.objects.filter(id=self.request.user.id)
        return User.objects.all()

class FileUploadViewSet(viewsets.ModelViewSet):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FileUploadDetailSerializer
        return FileUploadSerializer

    def get_queryset(self):
        # Users can only see their own uploads
        return FileUpload.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Set the user when creating a new upload
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        """
        Endpoint to trigger PII detection processing for a file
        """
        file_upload = self.get_object()
        
        # Create processing log
        processing_log = ProcessingLog.objects.create(
            file_upload=file_upload,
            started_at=timezone.now()
        )

        try:
            # Update file status
            file_upload.status = 'processing'
            file_upload.save()

            # Initialize Gemini model
            model = genai.GenerativeModel('gemini-1.5-pro')

            # Read file content
            file_content = file_upload.file.read().decode('utf-8')

            # Create prompt for PII detection
            prompt = f"""
            Analyze the following text for any personally identifiable information (PII).
            Identify instances of:
            - Email addresses
            - Phone numbers
            - Social security numbers
            - Credit card numbers
            - Physical addresses
            - Personal names
            - Dates of birth
            - IP addresses
            - Other PII

            For each instance, provide:
            - The type of PII
            - The line number
            - A confidence score (0-1)
            - The surrounding context
            - A suggested masked value

            Text to analyze:
            {file_content}
            """

            # Get response from Gemini
            response = model.generate_content(prompt)
            
            # Process and store PII detections
            # Note: This is a simplified example. In production, you'd want to
            # parse the response more carefully and handle various edge cases
            for detection in response.text.split('\n'):
                if detection.strip():
                    PIIDetection.objects.create(
                        file_upload=file_upload,
                        pii_type='other',  # You'd want to parse this from the response
                        line_number=1,  # You'd want to parse this from the response
                        context=detection,
                        confidence_score=0.9,  # You'd want to parse this from the response
                    )

            # Update processing status
            file_upload.status = 'completed'
            file_upload.processed_at = timezone.now()
            file_upload.save()

            # Update processing log
            processing_log.completed_at = timezone.now()
            processing_log.success = True
            processing_log.save()

            return Response({
                'status': 'success',
                'message': 'File processed successfully'
            })

        except Exception as e:
            # Handle errors
            file_upload.status = 'failed'
            file_upload.save()

            processing_log.completed_at = timezone.now()
            processing_log.success = False
            processing_log.error_message = str(e)
            processing_log.save()

            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProcessingLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProcessingLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only see logs for their own uploads
        return ProcessingLog.objects.filter(file_upload__user=self.request.user)

class PIIDetectionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PIIDetectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only see detections for their own uploads
        return PIIDetection.objects.filter(file_upload__user=self.request.user)
