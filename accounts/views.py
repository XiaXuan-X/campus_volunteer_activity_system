from django.shortcuts import render,HttpResponse,redirect
from .models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password

def login_view(request):

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:
            login(request, user)

            if user.role == "organiser":
                return redirect("organiser:manage_activities")

            elif user.role == "volunteer":
                return redirect("activities:dashboard")

        else:
            return render(request, "accounts/login.html", {
                "error": "Invalid email or password",
                "email": email
            })

    return render(request, "accounts/login.html")

def register(request):

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        role = request.POST.get("role")

        if password != confirm_password:
            return render(request, "accounts/register.html", {
                "error": "Passwords do not match"
            })
            
        if User.objects.filter(email=email).exists():
            return render(request, "accounts/register.html", {
                "error": "Email already registered"
            })

        User.objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            password=password,
            role=role
        )

        return redirect("/accounts/login/")

    return render(request, "accounts/register.html")

def password_reset_view(request):

    if request.method == "POST":
        email = request.POST.get("email")
        code = request.POST.get("code")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # check if user exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, "accounts/password_reset_form.html", {
                "error": "Email not registered",
                "email": email
            })

        # verify code (temporary)
        if code != "123456":
            return render(request, "accounts/password_reset_form.html", {
                "error": "Invalid verification code",
                "email": email
            })

        # check password match
        if password1 != password2:
            return render(request, "accounts/password_reset_form.html", {
                "error": "Passwords do not match",
                "email": email
            })

        # update password
        user.set_password(password1)
        user.save()

        return redirect("/accounts/login/")

    return render(request, "accounts/password_reset_form.html")