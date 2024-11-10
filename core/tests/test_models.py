from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from core.models import FileUpload, ProcessingLog, PIIDetection

User = get_user_model()

class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            organization='Test Org'
        )

    def test_user_creation(self):
        """Test user model creation with custom fields"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.organization, 'Test Org')

    def test_user_str_representation(self):
        """Test user string representation"""
        self.assertEqual(str(self.user), 'testuser')

class FileUploadModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='uploaduser',
            email='upload@example.com',
            password='testpass123'
        )
        self.test_file = SimpleUploadedFile(
            "test_file.txt", 
            b"Test file content for PII detection", 
            content_type="text/plain"
        )
        self.file_upload = FileUpload.objects.create(
            user=self.user,
            file=self.test_file,
            original_filename='test_file.txt',
            file_type='text/plain',
            status='pending'
        )

    def test_file_upload_creation(self):
        """Test file upload model creation"""
        self.assertEqual(self.file_upload.user, self.user)
        self.assertEqual(self.file_upload.original_filename, 'test_file.txt')
        self.assertEqual(self.file_upload.status, 'pending')

    def test_file_upload_status_choices(self):
        """Test file upload status choices"""
        valid_statuses = ['pending', 'processing', 'completed', 'failed']
        for status in valid_statuses:
            self.file_upload.status = status
            self.file_upload.save()
            self.assertEqual(self.file_upload.status, status)

class ProcessingLogModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='loguser',
            email='log@example.com',
            password='testpass123'
        )
        self.test_file = SimpleUploadedFile(
            "log_file.txt", 
            b"Test file for processing log", 
            content_type="text/plain"
        )
        self.file_upload = FileUpload.objects.create(
            user=self.user,
            file=self.test_file,
            original_filename='log_file.txt',
            file_type='text/plain'
        )
        self.processing_log = ProcessingLog.objects.create(
            file_upload=self.file_upload,
            success=True,
            processing_time=1.5
        )

    def test_processing_log_creation(self):
        """Test processing log model creation"""
        self.assertEqual(self.processing_log.file_upload, self.file_upload)
        self.assertTrue(self.processing_log.success)
        self.assertEqual(self.processing_log.processing_time, 1.5)

class PIIDetectionModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='piiuser',
            email='pii@example.com',
            password='testpass123'
        )
        self.test_file = SimpleUploadedFile(
            "pii_file.txt", 
            b"Test file with email test@example.com", 
            content_type="text/plain"
        )
        self.file_upload = FileUpload.objects.create(
            user=self.user,
            file=self.test_file,
            original_filename='pii_file.txt',
            file_type='text/plain'
        )
        self.pii_detection = PIIDetection.objects.create(
            file_upload=self.file_upload,
            pii_type='email',
            line_number=1,
            context='test@example.com',
            confidence_score=0.95
        )

    def test_pii_detection_creation(self):
        """Test PII detection model creation"""
        self.assertEqual(self.pii_detection.file_upload, self.file_upload)
        self.assertEqual(self.pii_detection.pii_type, 'email')
        self.assertEqual(self.pii_detection.line_number, 1)
        self.assertEqual(self.pii_detection.confidence_score, 0.95)

    def test_pii_type_choices(self):
        """Test PII type choices"""
        valid_pii_types = [
            'email', 'phone', 'ssn', 'credit_card', 
            'address', 'name', 'dob', 'ip_address', 'other'
        ]
        for pii_type in valid_pii_types:
            self.pii_detection.pii_type = pii_type
            self.pii_detection.save()
            self.assertEqual(self.pii_detection.pii_type, pii_type)
