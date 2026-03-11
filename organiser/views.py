from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from activities.models import Activity
from datetime import datetime


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


def manage_activities(request):
    activities = Activity.objects.filter(organiser=request.user)
    return render(request, "organiser/manage_activities.html", {
        "activities": activities
    })


def activity_detail(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id, organiser=request.user)

    approved_count = 0
    if hasattr(activity, "applications"):
        approved_count = activity.applications.filter(status="approved").count()

    return render(request, "organiser/activity_detail.html", {
        "activity": activity,
        "approved_count": approved_count,
    })


def edit_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id, organiser=request.user)

    if request.method == "POST":
        activity.title = request.POST.get("title")
        activity.description = request.POST.get("description")
        activity.location = request.POST.get("location")
        activity.start_datetime = datetime.fromisoformat(request.POST.get("start_datetime"))
        activity.end_datetime = datetime.fromisoformat(request.POST.get("end_datetime"))
        activity.max_volunteers = request.POST.get("max_volunteers")
        activity.save()

        messages.success(request, "Activity updated successfully")
        return redirect("organiser:activity_detail", activity_id=activity.id)

    return render(request, "organiser/create_activity.html", {
        "mode": "edit",
        "activity": activity,
    })


def application_detail(request):
    return render(request, "organiser/application_detail.html")

def delete_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)

    activity.delete()

    return redirect("organiser:manage_activities")