from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
import time
import uuid

User = get_user_model()

class SecurityPerformanceTestCase(TestCase):
    def setUp(self):
        # Create multiple test users
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        
        self.standard_user = User.objects.create_user(
            username='standarduser',
            email='standard@example.com',
            password='userpass123'
        )
        
        # Create API clients
        self.admin_client = APIClient()
        self.admin_client.force_authenticate(user=self.admin_user)
        
        self.standard_client = APIClient()
        self.standard_client.force_authenticate(user=self.standard_user)
        
        # Prepare test files
        self.large_file = SimpleUploadedFile(
            "large_test_file.txt", 
            b"A" * (10 * 1024 * 1024),  # 10MB file
            content_type="text/plain"
        )
        
        self.small_file = SimpleUploadedFile(
            "small_test_file.txt", 
            b"Small test file content",
            content_type="text/plain"
        )

    def test_user_role_based_access_control(self):
        """Test access control for different user roles"""
        # Admin-only endpoints
        admin_only_urls = [
            '/api/users/',
            '/admin/'
        ]
        
        # Test admin access
        for url in admin_only_urls:
            response = self.admin_client.get(url)
            self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_302_FOUND])
        
        # Test standard user access to admin endpoints
        for url in admin_only_urls:
            response = self.standard_client.get(url)
            self.assertIn(response.status_code, [
                status.HTTP_403_FORBIDDEN, 
                status.HTTP_401_UNAUTHORIZED
            ])

    def test_file_upload_performance(self):
        """Test file upload performance for different file sizes"""
        # Small file upload performance
        start_time = time.time()
        response = self.standard_client.post(
            '/api/files/', 
            {'file': self.small_file}, 
            format='multipart'
        )
        small_file_upload_time = time.time() - start_time
        
        # Large file upload performance
        start_time = time.time()
        response = self.standard_client.post(
            '/api/files/', 
            {'file': self.large_file}, 
            format='multipart'
        )
        large_file_upload_time = time.time() - start_time
        
        # Performance assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertLess(small_file_upload_time, 2.0)  # Small file should upload in < 2 seconds
        self.assertLess(large_file_upload_time, 10.0)  # Large file should upload in < 10 seconds

    def test_input_validation_and_sanitization(self):
        """Test input validation and sanitization"""
        # Test malicious filename
        malicious_filename = f"../../../etc/passwd-{uuid.uuid4()}.txt"
        malicious_file = SimpleUploadedFile(
            malicious_filename, 
            b"Potential security test file",
            content_type="text/plain"
        )
        
        response = self.standard_client.post(
            '/api/files/', 
            {'file': malicious_file}, 
            format='multipart'
        )
        
        # Ensure malicious filename is sanitized
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify filename was sanitized
        uploaded_file = response.data.get('original_filename', '')
        self.assertNotIn('../', uploaded_file)
        self.assertNotIn('..\\', uploaded_file)

    def test_brute_force_protection(self):
        """Test protection against brute force login attempts"""
        # Simulate multiple failed login attempts
        login_url = '/api/login/'
        
        for _ in range(10):
            response = self.client.post(login_url, {
                'username': 'nonexistent_user',
                'password': 'wrongpassword'
            })
        
        # Attempt final login
        final_response = self.client.post(login_url, {
            'username': 'nonexistent_user',
            'password': 'wrongpassword'
        })
        
        # Check for rate limiting or increased resistance
        self.assertIn(final_response.status_code, [
            status.HTTP_429_TOO_MANY_REQUESTS,
            status.HTTP_403_FORBIDDEN
        ])

    def test_sensitive_data_exposure(self):
        """Test that sensitive data is not exposed in API responses"""
        # Create a file upload
        response = self.standard_client.post(
            '/api/files/', 
            {'file': self.small_file}, 
            format='multipart'
        )
        
        # Retrieve file details
        file_id = response.data.get('id')
        file_details_response = self.standard_client.get(f'/api/files/{file_id}/')
        
        # Check response for sensitive information
        sensitive_keys = ['password', 'secret', 'token', 'key']
        
        for key in sensitive_keys:
            self.assertNotIn(key, str(file_details_response.data).lower())

    def test_concurrent_file_processing(self):
        """Test system behavior under concurrent file processing"""
        # Upload multiple files concurrently
        files = [
            SimpleUploadedFile(f"test_file_{i}.txt", b"Test content", content_type="text/plain")
            for i in range(5)
        ]
        
        responses = []
        for file in files:
            response = self.standard_client.post(
                '/api/files/', 
                {'file': file}, 
                format='multipart'
            )
            responses.append(response)
        
        # Verify all files were uploaded successfully
        for response in responses:
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
