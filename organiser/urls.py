from django.urls import path
from . import views

app_name = "organiser"

urlpatterns = [
    path("applications", views.organiser_applications, name="applications"),
    path("create/", views.create_activity, name="create_activity"),
    path("manage/", views.manage_activities, name="manage_activities"),
    path("detail/", views.organiser_activity_detail, name="activity_detail"),
    path("edit/", views.edit_activity, name="edit_activity"),
    path("application_detail/", views.application_detail, name="application_detail"),
]