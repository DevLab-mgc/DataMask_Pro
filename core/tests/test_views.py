from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from core.models import FileUpload, ProcessingLog, PIIDetection

User = get_user_model()

class FileUploadViewSetTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create API client and authenticate
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # Prepare test file
        self.test_file = SimpleUploadedFile(
            "test_file.txt", 
            b"Test file content for upload", 
            content_type="text/plain"
        )

    def test_file_upload_success(self):
        """Test successful file upload"""
        url = reverse('fileupload-list')
        
        # Prepare file upload data
        data = {
            'file': self.test_file,
            'original_filename': 'test_file.txt',
            'file_type': 'text/plain'
        }
        
        # Perform file upload
        response = self.client.post(url, data, format='multipart')
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify file upload was created
        self.assertTrue(FileUpload.objects.filter(user=self.user).exists())
        
        # Check file details
        file_upload = FileUpload.objects.get(user=self.user)
        self.assertEqual(file_upload.original_filename, 'test_file.txt')
        self.assertEqual(file_upload.file_type, 'text/plain')
        self.assertEqual(file_upload.status, 'pending')

    def test_file_upload_unauthorized(self):
        """Test file upload without authentication"""
        # Create unauthenticated client
        unauth_client = APIClient()
        
        url = reverse('fileupload-list')
        
        # Attempt file upload
        response = unauth_client.post(url, 
            {'file': self.test_file}, 
            format='multipart'
        )
        
        # Check unauthorized response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_file_upload_process(self):
        """Test file processing endpoint"""
        # Create a file upload first
        file_upload = FileUpload.objects.create(
            user=self.user,
            file=self.test_file,
            original_filename='test_file.txt',
            file_type='text/plain',
            status='pending'
        )
        
        # Get URL for processing
        url = reverse('fileupload-process', kwargs={'pk': file_upload.pk})
        
        # Trigger processing
        response = self.client.post(url)
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh file upload
        file_upload.refresh_from_db()
        
        # Check processing status
        self.assertEqual(file_upload.status, 'completed')
        
        # Check processing log was created
        self.assertTrue(ProcessingLog.objects.filter(file_upload=file_upload).exists())

class ProcessingLogViewSetTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='loguser',
            email='log@example.com',
            password='testpass123'
        )
        
        # Create API client and authenticate
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # Create test file and upload
        test_file = SimpleUploadedFile(
            "log_file.txt", 
            b"Test file for processing log", 
            content_type="text/plain"
        )
        self.file_upload = FileUpload.objects.create(
            user=self.user,
            file=test_file,
            original_filename='log_file.txt',
            file_type='text/plain'
        )
        
        # Create processing logs
        self.processing_log = ProcessingLog.objects.create(
            file_upload=self.file_upload,
            success=True,
            processing_time=1.5
        )

    def test_processing_log_list(self):
        """Test retrieving processing logs"""
        url = reverse('processinglog-list')
        
        # Get processing logs
        response = self.client.get(url)
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class PIIDetectionViewSetTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='piiuser',
            email='pii@example.com',
            password='testpass123'
        )
        
        # Create API client and authenticate
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # Create test file and upload
        test_file = SimpleUploadedFile(
            "pii_file.txt", 
            b"Test file with email test@example.com", 
            content_type="text/plain"
        )
        self.file_upload = FileUpload.objects.create(
            user=self.user,
            file=test_file,
            original_filename='pii_file.txt',
            file_type='text/plain'
        )
        
        # Create PII detection
        self.pii_detection = PIIDetection.objects.create(
            file_upload=self.file_upload,
            pii_type='email',
            line_number=1,
            context='test@example.com',
            confidence_score=0.95
        )

    def test_pii_detection_list(self):
        """Test retrieving PII detections"""
        url = reverse('piidetection-list')
        
        # Get PII detections
        response = self.client.get(url)
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
        # Verify PII detection details
        pii_data = response.data[0]
        self.assertEqual(pii_data['pii_type'], 'email')
        self.assertEqual(pii_data['line_number'], 1)
        self.assertEqual(pii_data['confidence_score'], 0.95)
