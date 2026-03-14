from django.urls import path
from . import views

app_name = "organiser"

urlpatterns = [
    path("applications", views.organiser_applications, name="applications"),
    path("create/", views.create_activity, name="create_activity"),
    path("manage/", views.manage_activities, name="manage_activities"),
    path("detail/<int:activity_id>/", views.activity_detail, name="activity_detail"),
    path("edit/<int:activity_id>/", views.edit_activity, name="edit_activity"),
    path("delete/<int:activity_id>/", views.delete_activity, name="delete_activity"),
    path("activity/<int:activity_id>/applications/", views.activity_applications, name="activity_applications",
    ),
    path("applications/<int:activity_id>/", views.application_detail, name="application_detail",
    ),
    path("applications/approve/<int:application_id>/", views.approve_application, name="approve_application",
),
path(
    "applications/reject/<int:application_id>/", views.reject_application, name="reject_application",
),
path("applications/attendance/<int:application_id>/", views.toggle_attendance, name="toggle_attendance",
),
]