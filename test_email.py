#!/usr/bin/env python
"""Test script to verify email functionality"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clinic_system.settings')
sys.path.insert(0, r'c:\Users\hp\Desktop\dental_clinic_system-main')

django.setup()

from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

User = get_user_model()

print('=' * 70)
print('EMAIL CONFIGURATION & TESTING FOR DENTAL CLINIC SYSTEM')
print('=' * 70)
print()

# Display configuration
print('📧 Current Email Configuration:')
print(f'   Backend: {settings.EMAIL_BACKEND}')
print(f'   Host: {settings.EMAIL_HOST}')
print(f'   Port: {settings.EMAIL_PORT}')
print(f'   User: {settings.EMAIL_HOST_USER}')
print(f'   TLS: {settings.EMAIL_USE_TLS}')
print(f'   From Email: {settings.DEFAULT_FROM_EMAIL}')
print()

# Test 1: Send simple test email
print('Test 1: Sending simple test email...')
try:
    result = send_mail(
        'Test Email - Dental Clinic System',
        'This is a test email to verify your password reset functionality is working correctly.\n\n'
        'If you receive this email, your system is configured properly to send password reset emails.\n\n'
        'Test sent at: ' + str(__import__('datetime').datetime.now()),
        settings.DEFAULT_FROM_EMAIL,
        ['magicnft8@gmail.com'],
        fail_silently=False
    )
    print(f'✅ Test email sent successfully! ({result} message)')
except Exception as e:
    print(f'❌ Error: {type(e).__name__}: {str(e)}')

print()

# Check if a user with the email exists
print('Test 2: Checking for admin/test user...')
try:
    user = User.objects.filter(email='magicnft8@gmail.com').first()
    if user:
        print(f'✅ Found user: {user.username} ({user.email})')
    else:
        print('⚠️  No user found with email magicnft8@gmail.com')
        print('   You can create one or use the admin interface to add a test user')
except Exception as e:
    print(f'❌ Error checking user: {str(e)}')

print()
print('=' * 70)
print('✅ EMAIL SETUP COMPLETE!')
print('=' * 70)
print()
print('📝 To test the full password reset flow:')
print('   1. Go to: http://localhost:8000/password_reset/')
print('   2. Enter: magicnft8@gmail.com')
print('   3. Click "Reset Password"')
print('   4. Check your Gmail inbox for the reset link')
print()
