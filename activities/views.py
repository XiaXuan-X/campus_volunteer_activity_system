from django.shortcuts import render, redirect

def dashboard(request):
    return render(request, "activities/dashboard.html")

def activity_list(request):
    return render(request, "activities/activity_list.html")

def activity_detail(request):
    return render(request, "activities/activity_detail.html")

def my_applications(request):
    return render(request, "activities/my_applications.html")

def profile(request):
    return render(request, "activities/profile.html")

def logout_view(request):
    return redirect("login")

def apply(request):
    if request.method == "POST":
        return redirect("activities:my_applications")
    return render(request, "activities/apply.html")