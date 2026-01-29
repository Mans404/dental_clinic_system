# 🔧 Setting Up Gmail App Password for Email Reset

## ⚠️ Current Issue
Your Django system is configured correctly, but Gmail is rejecting the password because:
- Gmail doesn't allow regular passwords for SMTP connections
- You must use an **App Password** instead

## ✅ Solution: Create Gmail App Password

Follow these steps to generate an App Password:

### Step 1: Enable 2-Factor Authentication (if not already enabled)
1. Go to: https://myaccount.google.com/security
2. Look for "How you sign in to Google"
3. If "2-Step Verification" is OFF, click it and turn it ON
4. Follow Google's instructions to set it up

### Step 2: Generate App Password
1. Go to: https://myaccount.google.com/apppasswords
2. Select:
   - **App**: Mail (or Gmail)
   - **Device**: Windows Computer (or your device type)
3. Google will generate a 16-character password
4. Copy this password (it looks like: `xxxx xxxx xxxx xxxx`)

### Step 3: Update Django Settings
1. Open: `clinic_system\settings.py`
2. Find the line: `EMAIL_HOST_PASSWORD = '2eUpZbp3x#HaP-manss'`
3. Replace it with your 16-character App Password:
   ```python
   EMAIL_HOST_PASSWORD = 'your-16-char-app-password-here'
   ```
4. Remove spaces if Google includes them (it should just be letters/numbers)

### Step 4: Test the Connection
After updating the password, run:
```bash
python test_email.py
```

You should see:
```
✅ Test email sent successfully!
```

## 📧 How to Use Password Reset After Setup

1. Start the Django server:
   ```bash
   python manage.py runserver
   ```

2. Go to: `http://localhost:8000/password_reset/`

3. Enter your email: `magicnft8@gmail.com`

4. Click "Reset Password"

5. Check your Gmail inbox for the password reset email with a link

6. Click the link and set a new password

## 🔒 Security Notes
- App Passwords are specific to this application only
- If you ever need to revoke it, do so in your Google Account settings
- Never share your App Password
- The regular account credentials won't work with SMTP

---
**Need help?** See: https://support.google.com/accounts/answer/185833
