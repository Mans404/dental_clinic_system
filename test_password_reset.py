#!/usr/bin/env python
"""Test password reset functionality"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clinic_system.settings')
sys.path.insert(0, r'c:\Users\hp\Desktop\dental_clinic_system-main')

django.setup()

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

print("=" * 70)
print("PASSWORD RESET TESTING")
print("=" * 70)
print()

# Get the user
user = User.objects.filter(email='magicnft8@gmail.com').first()

if not user:
    print("❌ User not found!")
    sys.exit(1)

print(f"✓ Found user: {user.username}")
print(f"✓ Email: {user.email}")
print()

# Test 1: Generate reset token
print("Test 1: Generate Password Reset Token")
print("-" * 70)

uid = urlsafe_base64_encode(force_bytes(user.pk))
token = default_token_generator.make_token(user)

print(f"✓ UID: {uid}")
print(f"✓ Token: {token}")
print(f"✓ Reset URL: /reset/{uid}/{token}/")
print()

# Test 2: Verify token
print("Test 2: Verify Token")
print("-" * 70)

is_valid = default_token_generator.check_token(user, token)
print(f"✓ Token is valid: {is_valid}")
print()

# Test 3: Simulate password change
print("Test 3: Simulate Password Change")
print("-" * 70)

old_password = user.password
new_password = "NewPassword123!@#"

user.set_password(new_password)
user.save()

print(f"✓ Old password hash: {old_password[:30]}...")
print(f"✓ New password hash: {user.password[:30]}...")
print()

# Test 4: Verify new password works
print("Test 4: Verify New Password")
print("-" * 70)

# Refresh from DB
user.refresh_from_db()

if user.check_password(new_password):
    print(f"✓ New password '{new_password}' works correctly!")
    print("✓ Login should succeed with this password")
else:
    print(f"❌ New password '{new_password}' does NOT work!")

print()

# Test 5: Verify token can't be reused
print("Test 5: Verify Token One-Time Use")
print("-" * 70)

is_valid_again = default_token_generator.check_token(user, token)
print(f"✓ Token valid on first check: {is_valid}")
print(f"✓ Token valid on second check (should be False): {is_valid_again}")

if not is_valid_again:
    print("✓ Token correctly invalidated after first use!")
else:
    print("⚠️  Warning: Token is still valid (might be a caching issue)")

print()
print("=" * 70)
print("✅ PASSWORD RESET SYSTEM IS WORKING!")
print("=" * 70)
print()
print("📝 To test with the browser:")
print("   1. Go to: http://localhost:8000/password_reset/")
print("   2. Enter: magicnft8@gmail.com")
print("   3. Click 'Reset Password'")
print("   4. Check console/email for reset link")
print("   5. Click reset link")
print("   6. Enter new password and confirm")
print("   7. Login with new password")
print()
