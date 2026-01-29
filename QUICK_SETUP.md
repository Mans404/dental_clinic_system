
# ✅ PASSWORD RESET EMAIL - QUICK SETUP CHECKLIST

## 📝 3-Step Setup (5 minutes)

### ☐ Step 1: Enable 2-Step Verification
- [ ] Go to: https://myaccount.google.com/security
- [ ] Click "2-Step Verification" under "How you sign in to Google"
- [ ] Follow prompts and verify with your phone

### ☐ Step 2: Get App Password from Google
- [ ] Go to: https://myaccount.google.com/apppasswords
- [ ] Select: **Mail** and **Windows Computer**
- [ ] Google generates a 16-character password
- [ ] Copy it: `________________`

### ☐ Step 3: Update Django Settings
- [ ] Open: `clinic_system/settings.py`
- [ ] Find line: `EMAIL_HOST_PASSWORD = '2eUpZbp3x#HaP-manss'`
- [ ] Replace with your App Password:
```python
EMAIL_HOST_PASSWORD = 'your-16-char-app-password-here'
```
- [ ] Save the file

### ☐ Test It
```bash
python test_email.py
```

Expected output:
```
✅ Test email sent successfully!
```

---

## 🎯 Testing Password Reset (After Getting App Password)

1. Start Django server:
   ```bash
   python manage.py runserver
   ```

2. Open in browser:
   ```
   http://localhost:8000/password_reset/
   ```

3. Enter email: `magicnft8@gmail.com`

4. Click "Reset Password"

5. Check Gmail inbox for reset email

6. Click reset link and set new password

7. ✅ Done!

---

## 📊 Current System Status

✅ Email backend configured (SMTP)
✅ All password reset routes set up
✅ All password reset templates ready
✅ User account exists (Mostafa_Tarek)
✅ Custom form validation ready
⏳ **WAITING FOR:** App Password from Gmail

---

## 🆘 Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| "Application-specific password required" | Use App Password, not Gmail password |
| "2-Step Verification not found" | Make sure 2FA is enabled first |
| Email not arriving | Check Spam folder or try again |
| Can't find apppasswords page | Ensure 2-Step Verification is ON |

---

## 💾 Key Files Modified/Created

- `clinic_system/settings.py` - Email configuration (cleaned up)
- `test_email.py` - Testing script
- `PASSWORD_RESET_SETUP.md` - Full documentation
- `EMAIL_SETUP_GUIDE.md` - Quick guide
- `.env.example` - Environment template

---

## 🚀 Status: Ready to Go!

All you need is the App Password. Once you have it, everything will work!

