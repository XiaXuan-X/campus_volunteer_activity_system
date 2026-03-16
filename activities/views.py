from django.shortcuts import render, redirect, get_object_or_404
from activities.models import Activity
from django.utils import timezone
from organiser.models import Application
from django.db.models import Count, Q, F
from django.contrib.auth.decorators import login_required
from accounts.models import User


def dashboard(request):
    now = timezone.now()

    applications = Application.objects.filter(volunteer=request.user)

    total_applications = applications.count()
    pending = applications.filter(status="pending").count()
    approved = applications.filter(status="approved").count()

    available_activities = Activity.objects.filter(
        start_datetime__lte=now,
        end_datetime__gte=now,
        end_datetime__gt=F("start_datetime")
    ).count()

    recent_applications = applications.order_by("-applied_at")[:3]

    upcoming_activities = Activity.objects.filter(
        start_datetime__gt=now,
        end_datetime__gt=F("start_datetime")
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
    activities = Activity.objects.annotate(
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

    now = timezone.localtime()

    for activity in activities:
        activity_start = timezone.localtime(activity.start_datetime)
        activity_end = timezone.localtime(activity.end_datetime)

        if activity_end <= activity_start:
            activity.display_status = "closed"
        elif activity_end < now:
            activity.display_status = "closed"
        elif activity_start > now:
            activity.display_status = "upcoming"
        elif activity.approved_volunteers >= activity.max_volunteers:
            activity.display_status = "full"
        else:
            activity.display_status = "open"

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

    now = timezone.localtime()
    activity_start = timezone.localtime(activity.start_datetime)
    activity_end = timezone.localtime(activity.end_datetime)

    if activity_end <= activity_start:
        display_status = "closed"
    elif activity_end < now:
        display_status = "closed"
    elif activity_start > now:
        display_status = "upcoming"
    elif approved_count >= activity.max_volunteers:
        display_status = "full"
    else:
        display_status = "open"

    is_full = display_status == "full"

    return render(request, "activities/activity_detail.html", {
        "activity": activity,
        "already_applied": already_applied,
        "is_full": is_full,
        "approved_count": approved_count,
        "display_status": display_status,
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


@login_required
def profile(request):
    user = request.user
    if request.method == "POST":
        user.phone = request.POST.get("phone")
        user.skills = request.POST.get("skills")
        user.previous_experience = request.POST.get("previous_experience")
        user.save()

    return render(request, "activities/profile.html", {
        "user": user
    })


def logout_view(request):
    return redirect("login")


def apply(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)

    already_applied = Application.objects.filter(
        volunteer=request.user,
        activity=activity
    ).exists()

    if already_applied:
        return redirect("activities:my_applications")

    approved_count = Application.objects.filter(
        activity=activity,
        status="approved"
    ).count()

    now = timezone.localtime()
    activity_start = timezone.localtime(activity.start_datetime)
    activity_end = timezone.localtime(activity.end_datetime)

    if activity_end <= activity_start:
        return redirect("activities:activity_detail", activity_id=activity.id)

    if activity_end < now:
        return redirect("activities:activity_detail", activity_id=activity.id)

    if activity_start > now:
        return redirect("activities:activity_detail", activity_id=activity.id)

    if approved_count >= activity.max_volunteers:
        return redirect("activities:activity_detail", activity_id=activity.id)

    Application.objects.create(
        volunteer=request.user,
        activity=activity,
        status="pending"
    )

    return redirect("activities:my_applications")


def view_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    context = {
        "profile_user": user
    }

    return render(request, "activities/view_profile.html", context)


def cancel_application(request, application_id):
    application = get_object_or_404(
        Application,
        id=application_id,
        volunteer=request.user
    )

    if application.status == "pending":
        application.status = "cancelled"
        application.save()

    return redirect("activities:my_applications")