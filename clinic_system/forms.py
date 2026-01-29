from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings


class CustomPasswordResetForm(PasswordResetForm):
    """Allow password reset only for a configured email address."""

    def clean_email(self):
        email = self.cleaned_data.get('email')
        allowed = getattr(settings, 'PASSWORD_RESET_ALLOWED_EMAIL', 'magicnft8@gmail.com')
        if email != allowed:
            raise forms.ValidationError(
                f"Password reset is allowed only for {allowed}."
            )
        return email
