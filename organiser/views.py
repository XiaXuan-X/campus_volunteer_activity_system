from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
def organiser_applications(request):
    return render(request, "organiser/applications.html")


def create_activity(request):
    if request.method == "POST":
        messages.success(request, "Activity created successfully")
        return redirect("organiser:manage_activities")

    return render(request, "organiser/create_activity.html", {
        "mode": "create"
    })

def manage_activities(request):
    return render(request, "organiser/manage_activities.html")

def organiser_activity_detail(request):
    return render(request, "organiser/activity_detail.html")

def edit_activity(request):
    if request.method == "POST":
        messages.success(request, "Activity updated successfully")
        return redirect("organiser:manage_activities")

    return render(request, "organiser/create_activity.html", {
        "mode": "edit"
    })

def application_detail(request):
    return render(request, "organiser/application_detail.html")
