from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User

# Create your views here.
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        return redirect("activities:dashboard")

    return render(request, "accounts/login.html")

def register_view(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password = request.POST["password"]

        User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        return redirect("login")
    return render(request,"accounts/register.html")

def password_reset_view(request):
    return render(request, "accounts/password_reset_form.html")