from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from activities.models import Activity
from organiser.models import Application
from datetime import datetime
import csv
from django.http import HttpResponse

def organiser_applications(request):
    activities = Activity.objects.filter(organiser=request.user)

    return render(
        request,
        "organiser/applications.html",
        {
            "activities": activities
        }
    )


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
    activity_data = []
    for activity in activities:
        approved_count = activity.applications.filter(status="approved").count()
        activity_data.append({
            "activity": activity,
            "approved_count": approved_count
        })

    return render(request, "organiser/manage_activities.html", {
        "activity_data": activity_data
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


def application_detail(request, activity_id):
    activity = get_object_or_404(
        Activity,
        id=activity_id,
        organiser=request.user
    )
    applications = activity.applications.all()

    return render(
        request,
        "organiser/application_detail.html",
        {
            "activity": activity,
            "applications": applications
        }
    )

def delete_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)

    activity.delete()

    return redirect("organiser:manage_activities")

def activity_applications(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id, organiser=request.user)
    applications = activity.applications.all()

    return render(
        request,
        "organiser/applications.html",
        {
            "activity": activity,
            "applications": applications,
        },
    )
    
def approve_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    activity = application.activity
    approved_count = Application.objects.filter(
        activity=activity,
        status="approved"
    ).count()
    if approved_count >= activity.max_volunteers:
        messages.error(request, "This activity is already full.")
        return redirect(
            "organiser:application_detail",
            activity_id=activity.id
        )
    application.status = "approved"
    application.save()
    messages.success(request, "Volunteer approved successfully.")

    return redirect(
        "organiser:application_detail",
        activity_id=activity.id
    )

def reject_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    application.status = "rejected"
    application.save()
    messages.success(request, "Volunteer rejected")

    return redirect(
        "organiser:application_detail",
        activity_id=application.activity.id
    )

def toggle_attendance(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    if request.method == "POST":

        application.attended = "attended" in request.POST
        application.save()

    return redirect(
        "organiser:application_detail",
        activity_id=application.activity.id
    )
    
def export_volunteers(request, activity_id):
    activity = Activity.objects.get(id=activity_id)
    applications = Application.objects.filter(activity=activity)
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{activity.title}_Applications.csv"'
    writer = csv.writer(response)
    writer.writerow([
        "Volunteer Name",
        "Email",
        "Status",
        "Attended",
        "Applied At",
    ])
    for application in applications:
        writer.writerow([
            application.volunteer.get_full_name(),
            application.volunteer.email,
            application.status,
            "Yes" if application.attended else "No",
            application.applied_at.strftime("%Y-%m-%d"),
        ])

    return response