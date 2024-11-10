from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """Custom user model for DataMask Pro"""
    email = models.EmailField(_('email address'), unique=True)
    organization = models.CharField(max_length=255, blank=True)
    api_key = models.CharField(max_length=255, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

class FileUpload(models.Model):
    """Model to track uploaded files for PII detection"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='file_uploads')
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    original_filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.original_filename} - {self.status}"

class ProcessingLog(models.Model):
    """Model to track processing operations and their outcomes"""
    file_upload = models.ForeignKey(FileUpload, on_delete=models.CASCADE, related_name='processing_logs')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    success = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)
    processing_time = models.FloatField(null=True, blank=True)  # in seconds

    def __str__(self):
        return f"Processing Log for {self.file_upload.original_filename}"

class PIIDetection(models.Model):
    """Model to store PII detection results"""
    PII_TYPES = [
        ('email', 'Email Address'),
        ('phone', 'Phone Number'),
        ('ssn', 'Social Security Number'),
        ('credit_card', 'Credit Card Number'),
        ('address', 'Physical Address'),
        ('name', 'Personal Name'),
        ('dob', 'Date of Birth'),
        ('ip_address', 'IP Address'),
        ('other', 'Other PII'),
    ]

    file_upload = models.ForeignKey(FileUpload, on_delete=models.CASCADE, related_name='pii_detections')
    pii_type = models.CharField(max_length=20, choices=PII_TYPES)
    line_number = models.IntegerField()
    column_number = models.IntegerField(null=True, blank=True)
    context = models.TextField()  # Surrounding text for context
    confidence_score = models.FloatField()
    masked_value = models.TextField(null=True, blank=True)  # The masked version of the PII
    detected_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['file_upload', 'line_number', 'column_number']

    def __str__(self):
        return f"{self.pii_type} in {self.file_upload.original_filename} at line {self.line_number}"
