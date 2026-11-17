# accounts/forms.py
from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import User
from myapp.models import Student
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
)


class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "••••••••"}
        ),
        validators=[validate_password],
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "••••••••"}
        )
    )

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]
        widgets = {
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "student@example.com"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "First Name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Last Name"}
            ),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip().lower()

        if not Student.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "Access denied: You are not enrolled as a student. Only registered students can create an account."
            )

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")
        return cleaned_data


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "name@example.com",
                "autocomplete": "email",
                "autofocus": True,
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "••••••••",
                "autocomplete": "current-password",
            }
        ),
    )

    error_messages = {
        "invalid_login": "Invalid email or password. Please try again.",
        "inactive": "This account is inactive.",
    }


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "name@example.com",
                "autocomplete": "email",
                "autofocus": True,
            }
        )


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": "••••••••",
                }
            )
