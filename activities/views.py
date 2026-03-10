from django.shortcuts import render, redirect
from activities.models import Activity
from django.utils import timezone
from django.shortcuts import get_object_or_404
from organiser.models import Application
from django.db.models import Count, Q

def dashboard(request):

    applications = Application.objects.filter(volunteer=request.user)

    total_applications = applications.count()
    pending = applications.filter(status="pending").count()
    approved = applications.filter(status="approved").count()

    available_activities = Activity.objects.filter(
        end_datetime__gte=timezone.now()
    ).count()

    recent_applications = applications.order_by("-applied_at")[:3]

    upcoming_activities = Activity.objects.filter(
        end_datetime__gte=timezone.now()
    ).order_by("start_datetime")[:3]

    return render(request, "activities/dashboard.html", {
        "total_applications": total_applications,
        "pending": pending,
        "approved": approved,
        "available_activities": available_activities,
        "recent_applications": recent_applications,
        "upcoming_activities": upcoming_activities
    })


def activity_list(request):

    activities = Activity.objects.filter(
        end_datetime__gte=timezone.now()
    ).annotate(
        approved_volunteers=Count(
            "applications",
            filter=Q(applications__status="approved")
        )
    )

    title = request.GET.get("title")
    location = request.GET.get("location")
    date = request.GET.get("date")

    if title:
        activities = activities.filter(title__icontains=title)

    if location:
        activities = activities.filter(location__icontains=location)

    if date:
        activities = activities.filter(
            start_datetime__date__lte=date,
            end_datetime__date__gte=date
        )

    activities = activities.order_by("start_datetime")

    return render(request, "activities/activity_list.html", {
        "activities": activities
    })

def activity_detail(request, activity_id):

    activity = get_object_or_404(Activity, id=activity_id)

    already_applied = Application.objects.filter(
        volunteer=request.user,
        activity=activity
    ).exists()

    approved_count = Application.objects.filter(
        activity=activity,
        status="approved"
    ).count()

    is_full = approved_count >= activity.max_volunteers

    return render(request, "activities/activity_detail.html", {
        "activity": activity,
        "already_applied": already_applied,
        "is_full": is_full,
        "approved_count": approved_count
    })


def my_applications(request):

    applications = Application.objects.filter(
        volunteer=request.user
    ).select_related("activity")

    status = request.GET.get("status")
    query = request.GET.get("q")

    if status:
        applications = applications.filter(status=status)

    if query:
        applications = applications.filter(
            activity__title__icontains=query
        )

    applications = applications.order_by("-applied_at")

    return render(request, "activities/my_applications.html", {
        "applications": applications
    })

def profile(request):
    return render(request, "activities/profile.html")

def logout_view(request):
    return redirect("login")

def apply(request, activity_id):

    activity = get_object_or_404(Activity, id=activity_id)

    # prevent duplicate applications
    already_applied = Application.objects.filter(
        volunteer=request.user,
        activity=activity
    ).exists()

    if already_applied:
        return redirect("activities:my_applications")

    Application.objects.create(
        volunteer=request.user,
        activity=activity,
        status="pending"
    )

    return redirect("activities:my_applications")