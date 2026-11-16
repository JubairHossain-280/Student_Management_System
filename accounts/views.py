# accounts/views.py
from .forms import StudentRegistrationForm, EmailAuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import Group
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings
from myapp.models import Student


def register_user(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            # Fetch the verified enrolled student record
            student_record = Student.objects.get(email__iexact=email)

            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])

            if not user.first_name:
                user.first_name = student_record.first_name
            if not user.last_name:
                user.last_name = student_record.last_name

            user.save()
            # SECURE: Automatically assign the 'Student' group in code
            student_group = Group.objects.get(name="Student")
            user.groups.add(student_group)
            messages.success(request, "Account created successfully!")
            return redirect(settings.LOGIN_URL)
    else:
        form = StudentRegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


def login_user(request):
    # If already logged in, redirect away from login page
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    if request.method == "POST":
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Automatically rotates session key for security

            # Safe redirect: check 'next' query param against open-redirect attacks
            next_url = request.GET.get("next") or request.POST.get("next")
            if next_url and url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)

            messages.success(request, f"Welcome back, {user.get_short_name()}!")
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            messages.error(request, "Invalid email or password.")
    else:
        form = EmailAuthenticationForm(request)

    return render(request, "accounts/login.html", {"form": form})


def logout_user(request):
    if request.method == "POST":
        logout(request)
        messages.info(request, "You have been logged out.")
        return redirect(settings.LOGOUT_REDIRECT_URL)
    return redirect("students")
