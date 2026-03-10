from django.urls import path
from . import views

app_name = "activities"
urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("activity_list/", views.activity_list, name="activity_list"),
    path("detail/<int:activity_id>/", views.activity_detail, name="activity_detail"),
    path("my_applications/", views.my_applications, name="my_applications"),
    path("profile/", views.profile, name="profile"),
    path("logout/", views.logout_view, name="logout"),
    path("apply/<int:activity_id>/", views.apply, name="apply")
]