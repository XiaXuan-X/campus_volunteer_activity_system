from django.shortcuts import render, redirect
from django.contrib import messages
from activities.models import Activity
from datetime import datetime

# Create your views here.
def organiser_applications(request):
    return render(request, "organiser/applications.html")


def create_activity(request):

    if request.method == "POST":

        title = request.POST.get("title")
        description = request.POST.get("description")
        location = request.POST.get("location")

        start_datetime = request.POST.get("start_datetime")
        end_datetime = request.POST.get("end_datetime")

        max_volunteers = request.POST.get("max_volunteers")

        # Convert string to datetime
        start_datetime = datetime.fromisoformat(start_datetime)
        end_datetime = datetime.fromisoformat(end_datetime)

        Activity.objects.create(
            title=title,
            description=description,
            location=location,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            max_volunteers=max_volunteers,
            organiser=request.user
        )

        messages.success(request, "Activity created successfully")

        return redirect("organiser:manage_activities")

    return render(request, "organiser/create_activity.html", {
        "mode": "create"
    })

from activities.models import Activity


def manage_activities(request):
    activities = Activity.objects.filter(organiser=request.user)
    return render(request, "organiser/manage_activities.html", {
        "activities": activities
    })

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
