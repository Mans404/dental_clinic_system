
# 🔄 Password Reset Email Flow Diagram

## How the Password Reset System Works

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER FORGETS PASSWORD                        │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│  User visits: http://localhost:8000/password_reset/             │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│     Browser displays Password Reset Form                        │
│                                                                 │
│    ["Enter your email to reset your password"]                 │
│     ┌──────────────────────────────────────┐                  │
│     │ magicnft8@gmail.com                  │                  │
│     └──────────────────────────────────────┘                  │
│     [Reset Password]                                           │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│  Form Validation                                                │
│  ✓ Email exists in database                                    │
│  ✓ Email = magicnft8@gmail.com (allowed)                       │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│  Django Password Reset Token Generation                         │
│  ✓ Creates unique token                                         │
│  ✓ Encodes user ID (uidb64)                                    │
│  ✓ Sets expiration (1 day)                                     │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│  Email Preparation                                              │
│  ✓ Creates email subject                                       │
│  ✓ Renders email template with reset link                      │
│  ✓ Includes reset URL:                                         │
│    http://localhost:8000/reset/<uidb64>/<token>/              │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│  SMTP Connection to Gmail                                       │
│  ┌────────────────────────────────────────────────┐            │
│  │ smtp.gmail.com:587 (TLS)                       │            │
│  │ User: magicnft8@gmail.com                      │            │
│  │ Password: [App Password from Google]           │            │
│  └────────────────────────────────────────────────┘            │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│  📧 EMAIL SENT                                                  │
│                                                                 │
│  From: magicnft8@gmail.com                                      │
│  To: magicnft8@gmail.com                                        │
│  Subject: Password reset on your site                           │
│                                                                 │
│  Body contains:                                                 │
│  ✓ Password reset link                                         │
│  ✓ Username                                                    │
│  ✓ Domain name                                                 │
│  ✓ Expiration time                                             │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│  User receives email in inbox (usually within 5-10 seconds)    │
│                                                                 │
│  ✓ Email arrives (may check Spam/Promotions)                  │
│  ✓ User clicks reset link from email                           │
│  ✓ Link contains unique token                                  │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│  User visits reset link:                                        │
│  /reset/<uidb64>/<token>/                                      │
│                                                                 │
│  Django validates:                                              │
│  ✓ Token is valid                                              │
│  ✓ Token has not expired (1 day)                               │
│  ✓ User still exists                                           │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│     Browser displays New Password Form                          │
│                                                                 │
│    ["Enter your new password"]                                 │
│     ┌──────────────────────────────────────┐                  │
│     │ New password: ••••••••                │                  │
│     │ Confirm:     ••••••••                │                  │
│     └──────────────────────────────────────┘                  │
│     [Change password]                                          │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│  Django validates new password                                  │
│  ✓ Strong enough                                               │
│  ✓ Matches confirmation                                        │
│  ✓ Not too similar to username                                 │
│  ✓ Not a common password                                       │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│  🔄 Update Database                                             │
│  ✓ Hash new password with PBKDF2                               │
│  ✓ Store in database                                           │
│  ✓ Invalidate token                                            │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│     ✅ SUCCESS PAGE                                             │
│                                                                 │
│    "Password reset complete!"                                  │
│    "You may now login with your new password"                  │
│    [Go to login page]                                          │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│  User logs in with new password                                │
│                                                                 │
│  ✅ Login succeeds                                              │
│  ✅ User can access dashboard                                   │
│  ✅ Done! 🎉                                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔑 Key Technical Details

### Token Security
- Unique per request
- Time-limited (1 day)
- Invalidated after use
- Contains user ID
- Cannot be reused

### Email Security
- TLS encryption to Gmail
- App-specific password (no master password needed)
- Email delivered only to registered address
- No passwords in email body

### Database Security
- Passwords hashed with PBKDF2 (Django default)
- Never stored in plaintext
- Tokens are separate from passwords

---

## 📊 System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                    Django Dental Clinic                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────┐    ┌──────────────────┐                │
│  │   URLs.py        │    │   Forms.py       │                │
│  │ - password_reset │    │ - Custom form    │                │
│  │ - token validate │    │ - Email validate │                │
│  └──────────────────┘    └──────────────────┘                │
│           ▲                      ▲                             │
│           │                      │                             │
│  ┌──────────────────────────────────────┐                    │
│  │     Django Auth Views                 │                    │
│  │  - PasswordResetView                  │                    │
│  │  - PasswordResetDoneView              │                    │
│  │  - PasswordResetConfirmView           │                    │
│  │  - PasswordResetCompleteView          │                    │
│  └──────────────────────────────────────┘                    │
│           │                      │                             │
│           └──────────────────────┘                             │
│                      │                                         │
│  ┌──────────────────────────────────────┐                    │
│  │     Settings.py - Email Config       │                    │
│  │  - SMTP Backend                      │                    │
│  │  - Gmail SMTP server                 │                    │
│  │  - TLS enabled                       │                    │
│  │  - App password                      │                    │
│  └──────────────────────────────────────┘                    │
│           │                      │                             │
└───────────┼──────────────────────┼─────────────────────────────┘
            │                      │
            ▼                      ▼
   ┌──────────────────┐   ┌──────────────────┐
   │  SQLite Database │   │  Gmail SMTP      │
   │  - User data     │   │  - Sends emails  │
   │  - Passwords     │   │  - TLS secure    │
   │  - Tokens        │   │  - Port 587      │
   └──────────────────┘   └──────────────────┘
```

---

## 🎯 Three Environments

### Development (Current)
- ✅ SMTP: Gmail
- ✅ Email backend: SMTP
- ✅ TLS: Enabled
- ✅ Testing: test_email.py

### Testing
- Can use console backend (emails printed to console)
- Or use Gmail SMTP with test account

### Production
- Same SMTP config (update EMAIL_HOST_USER if different)
- Use environment variables for credentials
- Enable HTTPS
- Consider email logging

---

## 🚀 Performance Notes

- Email sending is **synchronous** (blocks until sent)
- For production, consider **Celery** for async email
- Typical email delivery: 1-2 seconds
- Gmail SMTP is very reliable

---

## 🔒 Security Checklist

✅ Passwords hashed with PBKDF2
✅ Tokens are unique and time-limited
✅ Email required for account recovery
✅ App passwords (not master password)
✅ TLS encryption for SMTP
✅ Custom form validation
✅ Tokens invalidated after use
✅ Reset links expire after 1 day

---

## Next Step

Once you get your **App Password** from Google, the entire system is ready to send real emails!

See: **QUICK_SETUP.md** for the 3 steps to complete setup.

